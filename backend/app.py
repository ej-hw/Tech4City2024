from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
import numpy as np
import cv2
import os
import sqlite3
from datetime import datetime

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)
Swagger(app)

# Ensure the backend directory exists
backend_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(backend_dir, 'database.db')

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY,
            name TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_submission(name):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO submissions (name, timestamp)
        VALUES (?, ?)
    ''', (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_files(path):
    return app.send_static_file(path)

@app.route('/detect', methods=['POST'])
def detect():
    """
    Detect head position
    ---
    parameters:
      - name: image
        in: formData
        type: file
        required: true
    responses:
      200:
        description: The result of head position detection
    """
    # Save the uploaded image
    image_file = request.files['image']
    image_path = os.path.join(backend_dir, 'input_image.jpg')
    image_file.save(image_path)

    # Perform head position detection
    posture, cropped_image = detect_head_position(image_path)

    # Save the cropped image if head is centralised
    if posture == 'Centralised':
        cv2.imwrite(os.path.join(backend_dir, 'centralised_image.jpg'), cropped_image)

    # Clean up
    if os.path.exists(image_path):
        os.remove(image_path)

    return jsonify({'posture': posture})

def detect_head_position(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    head_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    heads = head_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(heads) == 0:
        return "No head detected", image
    
    (x, y, w, h) = heads[0]
    head_center_x = x + w // 2
    mid_x = width // 2

    # Crop the image to the center frame (assuming 60% of width and 80% of height)
    crop_width = int(width * 0.6)
    crop_height = int(height * 0.8)
    start_x = max(0, mid_x - crop_width // 2)
    start_y = max(0, height // 2 - crop_height // 2)
    cropped_image = image[start_y:start_y + crop_height, start_x:start_x + crop_width]

    if abs(head_center_x - mid_x) > width * 0.1:
        return "Not centre", cropped_image
    else:
        return "Centralised", cropped_image

@app.route('/make_id', methods=['POST'])
def make_id():
    """
    Make Photo ID
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Photo ID created successfully
      400:
        description: No centralised image available
    """
    name = request.form['name']
    if os.path.exists(os.path.join(backend_dir, 'centralised_image.jpg')):
        save_submission(name)
        return send_from_directory(directory=backend_dir, path='centralised_image.jpg', as_attachment=True, download_name=f"{name}_ID.jpg")
    else:
        return jsonify({'error': 'No centralised image available'}), 400

@app.route('/submissions', methods=['GET'])
def get_submissions():
    """
    Get all submissions
    ---
    responses:
      200:
        description: List of all submissions
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT name, timestamp FROM submissions')
    submissions = cursor.fetchall()
    conn.close()
    return jsonify(submissions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
