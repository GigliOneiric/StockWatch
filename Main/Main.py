# from Twitter.TweetStreamListener import TweetStreamListener
from TextPreprocessing import TextPreprocess
from TextPreprocessing.Helpers.StopWords import StopWords

class Main:
    s = StopWords(text).remove_stopwords()
    print(s)

