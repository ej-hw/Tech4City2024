import sqlite3
import pandas as pd
import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from bs4 import BeautifulSoup
import re
from nltk.tokenize.toktok import ToktokTokenizer
import logging
import os

nltk.download('stopwords')
nltk.download('punkt')

# Initialize global models dictionary
models = {}

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def load_and_preprocess_data(db_file):
    logging.debug("Connecting to the database...")
    logging.debug(f"Database file path: {db_file}")
    
    # Verify if the file exists
    if not os.path.exists(db_file):
        logging.error(f"Database file does not exist: {db_file}")
        raise FileNotFoundError(f"Database file does not exist: {db_file}")
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    
    # Load data from the database
    logging.debug("Loading data from the database...")
    query = "SELECT * FROM imdb_reviews"
    imdb_data = pd.read_sql_query(query, conn)
    
    # Close the connection
    conn.close()
    logging.debug("Data loaded from the database.")

    # Preprocess data
    logging.debug("Starting preprocessing...")
    imdb_data = preprocess_data(imdb_data)
    train_reviews, train_sentiments, test_reviews, test_sentiments = split_data(imdb_data)
    logging.debug("Preprocessing completed.")

    return imdb_data, train_reviews, train_sentiments, test_reviews, test_sentiments

def preprocess_data(imdb_data):
    logging.debug("Initial sentiments distribution: {}".format(imdb_data['sentiment'].value_counts()))
    imdb_data['review'] = imdb_data['review'].apply(lambda x: denoise_text(x) if x else "")
    imdb_data['review'] = imdb_data['review'].apply(lambda x: remove_special_characters(x) if x else "")
    imdb_data['review'] = imdb_data['review'].apply(lambda x: simple_stemmer(x) if x else "")
    imdb_data['review'] = imdb_data['review'].apply(lambda x: remove_stopwords(x) if x else "")
    imdb_data['sentiment'] = imdb_data['sentiment'].apply(encode_sentiment)
    logging.debug("Sentiments distribution after encoding: {}".format(imdb_data['sentiment'].value_counts()))
    return imdb_data


def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', '', text)

def remove_special_characters(text, remove_digits=True):
    pattern = r'[^a-zA-z0-9\s]'
    text = re.sub(pattern, '', text)
    return text

def simple_stemmer(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text

def remove_stopwords(text, is_lower_case=False):
    tokenizer = ToktokTokenizer()
    stopword_list = set(nltk.corpus.stopwords.words('english'))
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def encode_sentiment(sentiment):
    sentiment = sentiment.strip().lower()
    if sentiment == 'positive':
        return 1
    elif sentiment == 'negative':
        return 0
    else:
        raise ValueError(f"Unknown sentiment value: {sentiment}")


def split_data(imdb_data):
    logging.debug("Splitting data into training and testing sets...")
    train_reviews = imdb_data.review[:40000]
    train_sentiments = imdb_data.sentiment[:40000]
    test_reviews = imdb_data.review[40000:]
    test_sentiments = imdb_data.sentiment[40000:]
    logging.debug("Training sentiments distribution after splitting: {}".format(train_sentiments.value_counts()))
    logging.debug("Testing sentiments distribution after splitting: {}".format(test_sentiments.value_counts()))
    return train_reviews, train_sentiments, test_reviews, test_sentiments


def vectorize_data(train_reviews, test_reviews):
    logging.debug("Vectorizing data...")
    all_reviews = pd.concat([train_reviews, test_reviews])
    cv = CountVectorizer(min_df=1, max_df=1.0, binary=False, ngram_range=(1, 3))
    tv = TfidfVectorizer(min_df=1, max_df=1.0, use_idf=True, ngram_range=(1, 3))
    
    cv.fit(all_reviews)
    tv.fit(all_reviews)
    
    cv_train_reviews = cv.transform(train_reviews)
    cv_test_reviews = cv.transform(test_reviews)
    
    tv_train_reviews = tv.transform(train_reviews)
    tv_test_reviews = tv.transform(test_reviews)
    logging.debug("Vectorization completed.")
    return cv_train_reviews, cv_test_reviews, tv_train_reviews, tv_test_reviews, cv, tv

def label_sentiments(sentiments):
    lb = LabelBinarizer()
    sentiment_data = lb.fit_transform(sentiments)
    return sentiment_data

def train_models(train_reviews, train_sentiments):
    logging.debug("Starting model training...")
    logging.debug(f"Training sentiments distribution before vectorization: {train_sentiments.value_counts()}")
    cv_train_reviews, _, tv_train_reviews, _, cv, tv = vectorize_data(train_reviews, train_reviews)
    lr = LogisticRegression(penalty='l2', max_iter=500, C=1, random_state=42)
    lr_bow = lr.fit(cv_train_reviews, train_sentiments)
    lr_tfidf = lr.fit(tv_train_reviews, train_sentiments)
    global models
    models = {'lr_bow': lr_bow, 'lr_tfidf': lr_tfidf, 'cv': cv, 'tv': tv}
    logging.debug("Model training completed.")
    return models


def evaluate_models(models, test_reviews, test_sentiments):
    logging.debug("Evaluating models...")
    cv = models['cv']
    tv = models['tv']
    
    cv_test_reviews = cv.transform(test_reviews)
    tv_test_reviews = tv.transform(test_reviews)
    
    lr_bow = models['lr_bow']
    lr_tfidf = models['lr_tfidf']
    
    lr_bow_predict = lr_bow.predict(cv_test_reviews)
    lr_tfidf_predict = lr_tfidf.predict(tv_test_reviews)
    
    lr_bow_score = accuracy_score(test_sentiments, lr_bow_predict)
    lr_tfidf_score = accuracy_score(test_sentiments, lr_tfidf_predict)
    
    lr_bow_report = classification_report(test_sentiments, lr_bow_predict, target_names=['Positive', 'Negative'])
    lr_tfidf_report = classification_report(test_sentiments, lr_tfidf_predict, target_names=['Positive', 'Negative'])
    
    cm_bow = confusion_matrix(test_sentiments, lr_bow_predict, labels=[1, 0])
    cm_tfidf = confusion_matrix(test_sentiments, lr_tfidf_predict, labels=[1, 0])
    
    results = {
        "lr_bow_score": lr_bow_score,
        "lr_tfidf_score": lr_tfidf_score,
        "lr_bow_report": lr_bow_report,
        "lr_tfidf_report": lr_tfidf_report,
        "cm_bow": cm_bow.tolist(),
        "cm_tfidf": cm_tfidf.tolist()
    }
    logging.debug("Model evaluation completed.")
    return results

def predict_sentiment(text, model_type='lr_tfidf'):
    cv = models['cv']
    tv = models['tv']
    if model_type == 'lr_bow':
        vectorizer = cv
    else:
        vectorizer = tv
    vectorized_text = vectorizer.transform([text])
    model = models.get(model_type)
    if model:
        prediction = model.predict(vectorized_text)
        return 'Positive' if prediction[0] == 1 else 'Negative'
    return 'Model not found'