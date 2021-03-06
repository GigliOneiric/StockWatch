# StockWatch

StockWatch is an open source stock market analysis software that uses Elasticsearch to store Twitter data and Tesla's stock price data. StockWatch performs sentiment analysis on the text to determine the general sentiment picture and displays the results in Kibana. 

## Download / Clone
```
git clone https://github.com/GigliOneiric/StockWatch.git
cd StockWatch
```
## Install - Docker
1. Download / Clone StockWatch repo 
2. Set up logstash, elasticsearch and kibana containers using Docker compose

```
cd StockWatch/Docker
docker-compose build && docker-compose up
```

## Requirements
```
pip install -r requirements.txt
```

## Setup
### API-Keys in Config-Folder
1. Rename twitter_api_keys (Demo).py to twitter_api_keys.py
2. Create a twitter application at https://developer.twitter.com/en/portal/dashboard
3. Insert Twitter API Keys to twitter_api_keys.py
```
consumer_key = "yourKEY"
consumer_secret = "yourKEY"
access_token = "yourKEY"
access_token_secret = "yourKEY"
bearer_token = "yourKEY"
```

### Change Twitter query in Twitter-Folder
- See: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule
- Note: Rules are stored until they are deleted
```
stream.add_rules(tweepy.StreamRule("(tesla OR #tesla) from:1542485416443625472"))
```

## Start
- Run main.py

## Kibana
Kibana can be accessed via the following link:
http://localhost:5601/app/dashboards

The login details are:
```
Username: elastic
Password: changeme
```

## ToDo
1. Setup KubeFlow
2. Create an own ML-Modell
3. Access the model with StockWatch via a REST API
