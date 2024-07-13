from flask import Flask, request, jsonify
from flask_cors import CORS
from model import get_sentiment_value
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (id INTEGER PRIMARY KEY, text TEXT, sentiment INTEGER, feedback TEXT, feedbacksentiment INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data['text']
    sentiment = get_sentiment_value(text)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO results (text, sentiment) VALUES (?, ?)", (text, sentiment))
    conn.commit()
    c.execute("SELECT last_insert_rowid()")
    analysis_id = c.fetchone()[0]
    conn.close()

    return jsonify({'id': analysis_id, 'text': text, 'sentiment': sentiment})

@app.route('/results', methods=['GET'])
def get_results():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM results ORDER BY id")
    results = c.fetchall()
    conn.close()

    return jsonify(results)

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    id = data['id']
    feedback = data['feedback']
    correct_feedback = data.get('correct_feedback')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if feedback == 'incorrect' and correct_feedback is not None:
        c.execute("UPDATE results SET feedback = 'incorrect', feedbacksentiment = ? WHERE id = ?", (int(correct_feedback), id))
    else:
        c.execute("UPDATE results SET feedback = 'correct' WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)
