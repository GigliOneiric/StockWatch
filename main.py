import json
from datetime import datetime
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

        ####################

            # extract the first hashtag from the object
            # transform the Hashtags into proper case

            dict_data_len = 0

            if 'hashtags' in dict_data['data']['entities']:
                dict_data_len = len(dict_data['data']['entities']['hashtags'])

            if dict_data_len > 0:
                for i in range(dict_data_len - 1):
                    hashtag = dict_data['data']['entities']['hashtags'][i]['tag'].title()
                    hashtags = list.append(hashtag)
            else:
                # Elasticeach does not take None object
                hashtags = ['None']

            # add text and sentiment info to elasticsearch
            es.index(index="logstash-a",
                     # create/inject data into the cluster with index as 'logstash-a'
                     # create the naming pattern in Management/Kinaba later in order to push the data to a dashboard
                     doc_type="test-type",
                     body={"author": dict_data["includes"]["users"][0]["name"],
                           "date": dict_data['data']['created_at'],
                           "text": dict_data['data']['text'],
                           "hashtags": hashtags,
                           "polarity": tweet.sentiment.polarity,
                           "subjectivity": tweet.sentiment.subjectivity,
                           "sentiment": sentiment})

        return True

    # on failure, print the error code and do not disconnect
    def on_errors(self, status):
        print(status)


stream = TweetStreamListener(bearer_token=bearer_token)
stream.add_rules(tweepy.StreamRule("tesla OR #tesla) AND from:1542485416443625472"))

while True:
    try:
        stream.filter(expansions=['author_id'], tweet_fields=['created_at', 'entities'])
        break
    except IncompleteRead:
        continue
    except KeyboardInterrupt:
        # or however you want to exit this loop
        stream.disconnect()
        break
