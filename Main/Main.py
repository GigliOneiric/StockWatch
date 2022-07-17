# from Twitter.TweetStreamListener import TweetStreamListener
from ELK import DashBoardService
from ELK.Correlation import check_correlation
from Stocks.StockStreamListener import listen_stream


class Main:
    DashBoardService.load_dashboard()
    listen_stream()
