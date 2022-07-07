import re
import emoji


def remove_emojis(text):
    emojis = re.compile("["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        u"\U00002500-\U00002BEF"  # chinese char
                        u"\U00002702-\U000027B0"
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                        u"\U0001f926-\U0001f937"
                        u"\U00010000-\U0010ffff"
                        u"\u2640-\u2642"
                        u"\u2600-\u2B55"
                        u"\u200d"
                        u"\u23cf"
                        u"\u23e9"
                        u"\u231a"
                        u"\ufe0f"  # dingbats
                        u"\u3030"
                        "]+", re.UNICODE)
    return re.sub(emojis, '', text)


def replace_emojis(text):
    # Group by same meaning
    text = re.sub('[\U0001F550-\U0001F567]', " of the clock ", text)

    # Replace emojis by their short text
    text = emoji.demojize(text)

    # Remove everything between emoji
    text = re.sub(
        r"(?<=:[a-zA-Z])(.*?)(?=:)",
        lambda g: "{}".format(re.sub(r"[^a-zA-Z]", "", g.group(1))),
        text,
    )

    # Remove : at the beginning and the end of an emoji
    text = text.replace(":", " ")

    return text