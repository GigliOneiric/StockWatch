import Config.text
from textblob import TextBlob


def analyzeSentiment(dict_data):
    # pass Tweet into TextBlob to predict the sentiment
    tweet = TextBlob(dict_data[Config.text.data][Config.text.text])

    # if the object contains Tweet
    if tweet:
        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = Config.text.negative
        elif tweet.sentiment.polarity == 0:
            sentiment = Config.text.neutral
        else:
            sentiment = Config.text.positive

        # print the predicted sentiment with the Tweets
        print(sentiment, tweet.sentiment.polarity, tweet)

        return tweet, sentiment
