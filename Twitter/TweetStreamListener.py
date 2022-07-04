import json
import tweepy
import Config.twitter_api_keys
import Config.text
from http.client import IncompleteRead

from ELK import TweetWriter
from Sentiment.sentimentAnalyzer import analyzeSentiment

consumer_key = Config.twitter_api_keys.consumer_key
consumer_secret = Config.twitter_api_keys.consumer_secret
access_token = Config.twitter_api_keys.access_token
access_token_secret = Config.twitter_api_keys.access_token_secret
bearer_token = Config.twitter_api_keys.bearer_token

client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret, wait_on_rate_limit=True)


class TweetStreamListener(tweepy.StreamingClient):

    def on_data(self, data):
        dict_data = json.loads(data)

        result = analyzeSentiment(dict_data)
        tweet = result[0]
        sentiment = result[1]

        TweetWriter.write_tweet(dict_data, tweet, sentiment)

        return True

    # on failure, print the error code and do not disconnect
    def on_errors(self, status):
        print(status)


stream = TweetStreamListener(bearer_token=bearer_token)
stream.add_rules(tweepy.StreamRule("tesla OR #tesla) AND from:1542485416443625472"))

while True:
    try:
        stream.filter(expansions=[Config.text.author_id], tweet_fields=[Config.text.created_at, Config.text.entities])
        break
    except IncompleteRead:
        continue
    except KeyboardInterrupt:
        # or however you want to exit this loop
        stream.disconnect()
        break
