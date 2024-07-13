import os
from datetime import datetime, timedelta
from icecream import ic 

from werkzeug import Response
from dotenv import load_dotenv

import sqlite3
from utils.news_scraping import get_article, get_metadata
from utils.validation import validate_date
from flask import Flask, render_template, request, redirect, g
from transformers import pipeline, BertweetTokenizer

load_dotenv()  # take environment variables
app = Flask(__name__)

tokenizer = BertweetTokenizer.from_pretrained('finiteautomata/bertweet-base-sentiment-analysis')
classifier = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis", truncation=True, max_length=128)
sentiment_mapping = {"POS": "POSITIVE", "NEG": "NEGATIVE", "NEU": "NEUTRAL"}

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.execute('''
            CREATE TABLE IF NOT EXISTS news_sentiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT,
                sentiment TEXT,
                published_at TEXT
            )
        ''')
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")
        current_date = request.form.get("current_date")

        if topic and current_date:
            return redirect(f"/fetch_news?topic={topic}&current_date={current_date}")

    return render_template("index.html")

@app.route("/fetch_news", methods=["GET"])
def fetch_news() -> Response | str:
    topic = request.args.get("topic")
    date = request.args.get("current_date")

    if not topic or not date:
        return redirect("/")
    
    validate_date(date)
    
    current_date = datetime.strptime(date, "%Y-%m-%d")

    # Hard fix start date to search news from 20 days ago
    start_date = current_date - timedelta(days=20)

    # Format to ISO8601
    start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    current_date = current_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Check api key
    api_key = os.getenv("NEWS_API_TOKEN")
    if not api_key:
        print("API key not found in environment variables")
        return redirect("/")

    metadata = get_metadata(api_key, topic, start_date, current_date)

    db = get_db()
    cursor = db.cursor()
    
    for article_data in metadata:
        raw_content = get_article(article_data['url'])
        processed_content = raw_content.replace('\n', ' ')
        sentiment_result = classifier(processed_content)[0]
        sentiment = sentiment_mapping.get(sentiment_result['label'], sentiment_result['label'])
        article_data['sentiment'] = sentiment
        article_data['content'] = processed_content

        cursor.execute('''
            INSERT INTO news_sentiments (title, url, sentiment, published_at)
            VALUES (?, ?, ?, ?)
        ''', (article_data['title'], article_data['url'], article_data['sentiment'], article_data['publishedAt']))
        db.commit()

    return render_template("index.html", news_data=metadata, sentiment=False)

@app.route("/analyze_sentiment", methods=["GET", "POST"])
def analyze_sentiment() -> Response | str:
    if request.method == "POST":
        metadata = request.form.get("metadata")
    if metadata:
        metadata = eval(metadata)
    return render_template("index.html", news_data=metadata, sentiment=True)

if __name__ == "__main__":
    app.run(debug=True)
