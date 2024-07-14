from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3
import base64
from datetime import datetime
import os
from model import detect_objects  # Import the detect_objects function from model.py

app = Flask(__name__, static_folder='../frontend')

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (date TEXT, objects TEXT, image TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if image_file:
        filename = secure_filename(image_file.filename)
        image_path = os.path.join('uploads', filename)
        image_file.save(image_path)
        
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
        
        objects, processed_image = detect_objects(image_data)
        processed_image_data = base64.b64encode(processed_image).decode('utf-8')
        
        # Store result in database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''INSERT INTO results (date, objects, image)
                     VALUES (?, ?, ?)''', (datetime.now().isoformat(), ','.join(objects), processed_image_data))
        conn.commit()
        conn.close()
        
        os.remove(image_path)  # Clean up the uploaded file
        
        return jsonify({'objects': objects, 'image': processed_image_data})

@app.route('/results', methods=['GET'])
def get_results():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT date, objects, image FROM results ORDER BY date DESC')
    results = [{'date': row[0], 'objects': row[1].split(','), 'image': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    init_db()
    os.makedirs('uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=8000, debug=True)
