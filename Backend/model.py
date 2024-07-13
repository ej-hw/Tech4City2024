from transformers import pipeline

def get_sentiment_value(text):
    sentiment_pipeline = pipeline("sentiment-analysis")
    sentiment = sentiment_pipeline(text)[0]

    if sentiment['label'] == 'POSITIVE':
        return 1
    elif sentiment['label'] == 'NEGATIVE':
        return -1
    else:
        return 0
