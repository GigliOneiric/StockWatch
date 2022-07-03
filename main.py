import json
import tweepy
import Config.twitter_api_keys
import Config.text
from http.client import IncompleteRead
from elasticsearch import Elasticsearch
from textblob import TextBlob

consumer_key = Config.twitter_api_keys.consumer_key
consumer_secret = Config.twitter_api_keys.consumer_secret
access_token = Config.twitter_api_keys.access_token
access_token_secret = Config.twitter_api_keys.access_token_secret
bearer_token = Config.twitter_api_keys.bearer_token

# create instance of elasticsearch
es = Elasticsearch(hosts="http://elastic:changeme@localhost:9200/")

client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret, wait_on_rate_limit=True)


class TweetStreamListener(tweepy.StreamingClient):

    def on_data(self, data):
        dict_data = json.loads(data)

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

            ####################

            # extract the first hashtag from the object
            # transform the Hashtags into proper case

            dict_data_len = 0

            if Config.text.hashtags in dict_data[Config.text.data][Config.text.entities]:
                dict_data_len = len(dict_data[Config.text.data][Config.text.entities][Config.text.hashtags])

            if dict_data_len > 0:
                for i in range(dict_data_len - 1):
                    hashtag = dict_data[Config.text.data][Config.text.entities][Config.text.hashtags][i][
                        Config.text.tag].title()
                    hashtags = list.append(hashtag)
            else:
                # Elasticeach does not take None object
                hashtags = [Config.text.none]

            doc = {
                   Config.text.author: dict_data[Config.text.includes][Config.text.users][0][Config.text.name],
                   Config.text.date: dict_data[Config.text.data][Config.text.created_at],
                   Config.text.text: dict_data[Config.text.data][Config.text.text],
                   Config.text.hashtags: hashtags,
                   Config.text.polarity: tweet.sentiment.polarity,
                   Config.text.subjectivity: tweet.sentiment.subjectivity,
                   Config.text.sentiment: sentiment,
                   }

            # add text and sentiment info to elasticsearch
            es.index(index="twitter", document=doc)

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
