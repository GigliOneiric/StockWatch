import Config.text
import pandas as pd
import eland as ed

from datetime import date
from elasticsearch import Elasticsearch

# create instance of elasticsearch
es = Elasticsearch(hosts="http://elastic:changeme@localhost:9200/")


def write_correlation():
    correlation = check_correlation()

    doc = {
        Config.text.id: 1,
        Config.text.date: date.today(),
        Config.text.correlation: str(correlation)
    }

    es.index(index="correlation", id=1, document=doc)


def check_correlation():
    df = pd.DataFrame()

    if es.indices.exists(index="twitter") and es.indices.exists(index="yahoo"):
        df = merge_polarity_close_by_date()

    if len(df) > 1:
        correlation = df[Config.text.close].corr(df['avg_polarity'], method='pearson')
    else:
        correlation = 0

    return correlation


def merge_polarity_close_by_date():
    df_polarity = polarity_by_date()
    df_close = close_by_date()

    df = pd.merge(df_polarity, df_close, on=[Config.text.date])

    return df


def polarity_by_date():
    # Connect to 'twitter' index via localhost Elasticsearch node
    df = ed.DataFrame('http://elastic:changeme@localhost:9200/', 'twitter')
    df = ed.eland_to_pandas(df)

    df[Config.text.date] = pd.to_datetime(df[Config.text.date]).dt.tz_convert('CET')
    df[Config.text.date] = df[Config.text.date].dt.date

    df = df.groupby(Config.text.date).mean().reset_index()
    df.columns = [Config.text.date, 'avg_polarity']

    return df


def close_by_date():
    # Connect to 'yahoo' index via localhost Elasticsearch node
    df = ed.DataFrame('http://elastic:changeme@localhost:9200/', 'yahoo')
    df = ed.eland_to_pandas(df)

    df[Config.text.date] = pd.to_datetime(df[Config.text.date]).dt.tz_localize('UTC').dt.tz_convert('CET')
    df[Config.text.date] = df[Config.text.date].dt.date

    df = df.reset_index()
    df = df[[Config.text.date, Config.text.close]].copy()

    return df
