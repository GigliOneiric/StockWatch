from Twitter.TweetStreamListener import TweetStreamListener
from ELK import DashBoardService
from Stocks.StockStreamListener import listen_stream


class Main:
    DashBoardService.load_dashboard()
    listen_stream()
