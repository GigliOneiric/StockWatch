import json
from http.client import IncompleteRead

import tweepy
from elasticsearch import Elasticsearch
from textblob import TextBlob

import Config.twitter_api_keys

consumer_key = Config.twitter_api_keys.consumer_key
consumer_secret = Config.twitter_api_keys.consumer_secret
access_token = Config.twitter_api_keys.access_token
access_token_secret = Config.twitter_api_keys.access_token_secret
bearer_token = Config.twitter_api_keys.bearer_token

# create instance of elasticsearch
es = Elasticsearch()

client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret, wait_on_rate_limit=True)


class TweetStreamListener(tweepy.StreamingClient):

    def on_data(self, data):
        dict_data = json.loads(data)

        # pass Tweet into TextBlob to predict the sentiment
        tweet = TextBlob(dict_data['data']['text'])

        # if the object contains Tweet
        if tweet:
            # determine if sentiment is positive, negative, or neutral
            if tweet.sentiment.polarity < 0:
                sentiment = "negative"
            elif tweet.sentiment.polarity == 0:
                sentiment = "neutral"
            else:
                sentiment = "positive"

            # print the predicted sentiment with the Tweets
            print(sentiment, tweet.sentiment.polarity, tweet)

        return True

    # on failure, print the error code and do not disconnect
    def on_errors(self, status):
        print(status)


stream = TweetStreamListener(bearer_token=bearer_token)
stream.add_rules(tweepy.StreamRule("tesla OR #tesla) AND from:1542485416443625472"))

while True:
    try:
        stream.filter(expansions=["author_id"], tweet_fields=["created_at"])
        break
    except IncompleteRead:
        continue
    except KeyboardInterrupt:
        # or however you want to exit this loop
        stream.disconnect()
        break
