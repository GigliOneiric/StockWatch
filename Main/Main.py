from Twitter.TweetStreamListener import TweetStreamListener
from ELK import DashBoardService
from Stocks.StockStreamListener import listen_stream
from Sentiment import sentimentAnalyzer_kfp

class Main:

    sentiment_analyzer = 'TextBlob' # TextBlob or KFP

    DashBoardService.load_dashboard()
    listen_stream()
