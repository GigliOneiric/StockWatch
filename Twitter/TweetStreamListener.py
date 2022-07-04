import json
from time import sleep

import tweepy
import Config.twitter_api_keys
import Config.text

from ELK import TweetWriter
from Sentiment.sentimentAnalyzer import analyzeSentiment
from http.client import IncompleteRead

consumer_key = Config.twitter_api_keys.consumer_key
consumer_secret = Config.twitter_api_keys.consumer_secret
access_token = Config.twitter_api_keys.access_token
access_token_secret = Config.twitter_api_keys.access_token_secret
bearer_token = Config.twitter_api_keys.bearer_token


class TweetStreamListener(tweepy.StreamingClient):

    def on_data(self, data):
        dict_data = json.loads(data)

        result = analyzeSentiment(dict_data)
        tweet = result[0]
        sentiment = result[1]

        TweetWriter.write_tweet(dict_data, tweet, sentiment)

        return True

    # on failure, print the error code and do not disconnect
    def on_errors(self, status_code):
        print(status_code)

    def on_request_error(self, status_code):
        if status_code == 429:
            print('Rate limits per 15 minute are reached')
            sleep(60 * 15)
        else:
            print(status_code)


stream = TweetStreamListener(bearer_token=bearer_token, wait_on_rate_limit=True)
stream.add_rules(tweepy.StreamRule("tesla OR #tesla) AND from:1542485416443625472"))

try:
    stream.filter(expansions=[Config.text.author_id],
                  tweet_fields=[Config.text.created_at, Config.text.entities], threaded=True)
except IncompleteRead:
    pass
except KeyboardInterrupt:
    stream.disconnect()
