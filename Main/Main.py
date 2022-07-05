# from Twitter.TweetStreamListener import TweetStreamListener
from Cleaning import TextPreprocess


class Main:
    pass

    text = "He likes Tobias https://github.com/ is coding this part. who are you @Tobias? I'll 123 <with> likes."

    print(TextPreprocess.preprocess(text))
