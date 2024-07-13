Flask News Sentiment Analysis App
=================================

This is a Flask web application that fetches news articles based on a given topic and date, analyzes the sentiment of the articles using a pretrained BERTweet model, and stores the results in a SQLite database.

Features
--------

*   Fetch news articles from around the world using the [NewsAPI](https://newsapi.org).
*   Scrape article content using BeautifulSoup.
*   Analyze article sentiment using the BERTweet model for sentiment analysis.
*   Store article metadata and sentiment in a SQLite database.

Setup Instructions
------------------

### Prerequisites

*   Python 3.12 or higher
*   A NewsAPI key. Sign up at [NewsAPI](https://newsapi.org/register) to get your API key.

### Installation

    
    git clone https://github.com/GeorgePPP/Tech4City2024
    cd Tech4City2024
    pip install -r requirements.txt
    

### Environment Variables

Create a `.env` file in the root directory of the project and add your NewsAPI key:

    
    NEWS_API_TOKEN=your_news_api_key
    

Running the Application
-----------------------

    
    python app.py
    

By default, the app runs on [http://127.0.0.1:5000](http://127.0.0.1:5000).

Usage
-----

### Home Page

On the home page, enter a topic and a date to search for news articles.

### Fetch News

After submitting the topic and date, the app will fetch news articles from NewsAPI, scrape their content, analyze their sentiment, and display the results.

Code Overview
-------------

### File Structure

    
    Tech4City2024/
    ├── templates/
    │   └── index.html
    ├── utils/
    │   ├── news_scraping.py
    │   └── validation.py
    ├── .env
    ├── app.py
    ├── database.db
    ├── requirements.txt
    └── README.html
    

### Main Files

*   `app.py`: The main Flask application file containing route definitions and core logic.
*   `utils/news_scraping.py`: Contains functions `get_metadata` and `get_article` for fetching news metadata and scraping article content, respectively.
*   `utils/validation.py`: Contains the `validate_date` function to ensure the date format is correct.
*   `templates/index.html`: The HTML template for rendering the home page and displaying results.

### Dependencies

Dependencies are listed in the `requirements.txt` file:

    
    flask
    python-dotenv
    sqlite3
    transformers
    icecream
    werkzeug
    beautifulsoup4