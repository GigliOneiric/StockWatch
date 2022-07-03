import Config.text
from elasticsearch import Elasticsearch

# create instance of elasticsearch
es = Elasticsearch(hosts="http://elastic:changeme@localhost:9200/")


def write_tweet(dict_data, tweet, sentiment):
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
