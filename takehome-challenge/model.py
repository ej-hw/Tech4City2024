from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.05:
        sentiment = 'Positive 😊'
    elif polarity < -0.05:
        sentiment = 'Negative 😔'
    else:
        sentiment = 'Neutral 😐'
    
    return {
        'sentiment': sentiment,
        'polarity': polarity,
        'subjectivity': analysis.sentiment.subjectivity
    }
