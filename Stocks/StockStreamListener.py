import datetime
import yfinance as yf
from elasticsearch import NotFoundError

from ELK import StockWriter


def on_data():
    tesla = yf.Ticker("TSLA")

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    start = datetime.datetime(2010, 1, 1)
    end = today

    try:
        last = StockWriter.read_last_stock_date()
        last = datetime.datetime.strptime(last, '%Y-%m-%dT%H:%M:%S').date()
    except NotFoundError:
        data = tesla.history(start=start, end=end)
        last = end
        StockWriter.write_stock(data)

    if last < yesterday:
        start = last + datetime.timedelta(days=1)
        end = yesterday
        data = tesla.history(start=start, end=end)
        StockWriter.write_stock(data)
