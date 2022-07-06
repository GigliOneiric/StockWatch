from Twitter.TweetStreamListener import TweetStreamListener
from Cleaning import TextPreprocess


class Main:
    text = "He '  :(    likes x_x #Tobi Tobias https://github.com/ is coding l33d this part. who are you @Tobias? I'll 123 forest <with> likes."

    print(TextPreprocess.preprocess(text))


