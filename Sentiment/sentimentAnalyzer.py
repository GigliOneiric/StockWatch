import Config.text
from textblob import TextBlob
from TextPreprocessing import TextPreprocess


def analyzeSentiment(dict_data):
    # pass Tweet into TextBlob to predict the sentiment
    tweet = TextBlob(dict_data[Config.text.data][Config.text.text])
    tweet_cleaned = TextBlob(TextPreprocess.preprocess(dict_data[Config.text.data][Config.text.text]))

    # if the object contains Tweet
    if tweet_cleaned:
        # determine if sentiment is positive, negative, or neutral
        if tweet_cleaned.sentiment.polarity < 0:
            sentiment = Config.text.negative
        elif tweet_cleaned.sentiment.polarity == 0:
            sentiment = Config.text.neutral
        else:
            sentiment = Config.text.positive

        # print the predicted sentiment with the Tweets
        print(sentiment, tweet_cleaned.sentiment.polarity, tweet_cleaned)

        return tweet.polarity, sentiment
