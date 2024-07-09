from flask import Flask, request, jsonify, send_from_directory, render_template
from model import load_and_preprocess_data, train_models, evaluate_models, predict_sentiment
import os
import logging

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    logging.debug(f"Current working directory: {os.getcwd()}")
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/train', methods=['POST'])
def train():
    data = request.json
    db_file = data.get('db_file', 'backend/database.db')
    imdb_data, train_reviews, train_sentiments, test_reviews, test_sentiments = load_and_preprocess_data(db_file)
    models = train_models(train_reviews, train_sentiments)
    results = evaluate_models(models, test_reviews, test_sentiments)
    return jsonify(results)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    review = data.get('review')
    sentiment = predict_sentiment(review)
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    logging.debug("Starting the Flask application")
    app.run(host='0.0.0.0', port=5000)
