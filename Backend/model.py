from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

def get_sentiment_value(text):
    print('adafd')
    sid = SentimentIntensityAnalyzer()
    print('sfsfd')
    sentiment_scores = sid.polarity_scores(text)
    
    # Determine the highest sentiment score
    highest_sentiment = max(sentiment_scores, key=lambda k: sentiment_scores[k] if k in ['neg', 'neu', 'pos'] else -1)
    print('adafd')
    if highest_sentiment == 'pos':
        return 1
    elif highest_sentiment == 'neg':
        return -1
    else:
        return 0

