# from Twitter.TweetStreamListener import TweetStreamListener
from TextPreprocessing import TextPreprocess
from TextPreprocessing.Helpers.StopWords import StopWords


class Main:
    text = 'Test :)'
    print(TextPreprocess.preprocess(text))
