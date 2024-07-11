from flask import Flask, request, jsonify, render_template
from model import analyze_sentiment
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data['text']
    analysis = analyze_sentiment(text)
    
    conn = get_db_connection()
    conn.execute('INSERT INTO sentiments (text, sentiment, polarity, subjectivity) VALUES (?, ?, ?, ?)',
                 (text[:500], analysis['sentiment'], analysis['polarity'], analysis['subjectivity']))
    conn.commit()
    conn.close()
    
    return jsonify(analysis)

@app.route('/history')
def history():
    conn = get_db_connection()
    sentiments = conn.execute('SELECT * FROM sentiments ORDER BY id DESC LIMIT 10').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in sentiments])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
