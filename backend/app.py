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
    return jsonify({'result': 'success'})

@app.route('/predict', methods=['POST'])
def predict():
    if not models or 'lr_tfidf' not in models:
        # Load models from DB if not cached in memory
        models['lr_bow'] = load_model_from_db('lr_bow', models_db_file)
        models['lr_tfidf'] = load_model_from_db('lr_tfidf', models_db_file)
        vectorizers['cv'] = load_model_from_db('cv', models_db_file)
        vectorizers['tv'] = load_model_from_db('tv', models_db_file)
        if None in (models['lr_bow'], models['lr_tfidf'], vectorizers['cv'], vectorizers['tv']):
            return jsonify({'error': 'Please train the model first.'}), 500
    
    data = request.json
    review = data.get('review')
    sentiment = predict_sentiment(review, model_type='lr_tfidf')
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    logging.debug("Starting the Flask application")
    app.run(host='0.0.0.0', port=8000)
