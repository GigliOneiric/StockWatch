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

## Kibana
Kibana can be accessed via the following link:
http://localhost:5601/app/dashboards

The login details are:
Username: elastic
Password: changeme

