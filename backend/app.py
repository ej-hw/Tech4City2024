from flask import Flask, request, jsonify, send_from_directory, render_template
from model import *
from convertcsv import *
import os
import logging

app = Flask(__name__)
csv_file = 'db/IMDB Dataset.csv'  # Replace with your CSV file path
db_file = 'db/database.db'  # Replace with your desired database file name
table_name = 'imdb_reviews'  # Replace with your desired table name
models_db_file = 'db/models.db'
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    logging.debug(f"Current working directory: {os.getcwd()}")
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/train', methods=['GET'])
def train():
    csv_to_sqlite(csv_file, db_file, table_name)

    # Load and preprocess data
    imdb_data, train_reviews, train_sentiments, test_reviews, test_sentiments = load_and_preprocess_data(db_file)

    # Train and save models
    train_and_save_models(train_reviews, train_sentiments, models_db_file)
    return "Training Done"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    review = data.get('review')
    sentiment = predict_sentiment(review, model_type='lr_tfidf', db_file=models_db_file)
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    logging.debug("Starting the Flask application")
    app.run(host='0.0.0.0', port=8000)
