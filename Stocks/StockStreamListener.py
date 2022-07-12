import yfinance as yf
from elasticsearch import NotFoundError
from datetime import date, datetime, timedelta
from threading import Timer

from ELK import StockWriter


def listen_stream():
    on_data()
    listen_stream_timer()


def listen_stream_timer():
    x = datetime.today()
    y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
    delta_t = y - x
    secs = delta_t.total_seconds()

    def repeat():
        listen_stream()
        on_data()

    t = Timer(secs, repeat)
    t.start()


def on_data():
    tesla = yf.Ticker("TSLA")

    today = date.today()
    yesterday = today - timedelta(days=1)

    start = datetime(2010, 1, 1)
    end = today

    try:
        last = StockWriter.read_last_stock_date()
        last = datetime.strptime(last, '%Y-%m-%dT%H:%M:%S').date()
    except NotFoundError:
        data = tesla.history(start=start, end=end)
        last = end
        StockWriter.write_stock(data)

    if last < yesterday:
        start = last + timedelta(days=1)
        end = yesterday
        data = tesla.history(start=start, end=end)
        StockWriter.write_stock(data)
