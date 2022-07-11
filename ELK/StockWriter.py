import Config.text
from elasticsearch import Elasticsearch

# create instance of elasticsearch
es = Elasticsearch(hosts="http://elastic:changeme@localhost:9200/")


def write_stock(data):
    for i in range(len(data.index)):
        doc = {
            Config.text.company: Config.text.tesla,
            Config.text.date: data.index[i],
            Config.text.open: data['Open'][i],
            Config.text.high: data['High'][i],
            Config.text.low: data['Low'][i],
            Config.text.close: data['Close'][i]
        }

        # add text and sentiment info to elasticsearch
        es.index(index="yahoo", id=data.index[i], document=doc)


def read_last_stock_date():
    result = es.search(
        index='yahoo',
        body={
            "size": 1,
            "sort": {"date": "desc"},
            "query": {
                "match_all": {}
            }
        }
    )

    return result['hits']['hits'][0]['_source']['date']
