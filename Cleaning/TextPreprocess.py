import re
import unicodedata

import emoji
import nltk
import contractions
from string import punctuation
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob


def preprocess(text):
    downloadNLTK()

    text = remove_html_tags(text)
    text = replace_url(text)
    text = replace_atUser(text)
    text = replace_smiley(text)
    text = replace_emojis(text)
    # text = remove_leetspeak(text)
    text = remove_numbers(text)
    text = replace_contractions(text)
    text = remove_punct(text)
    text = to_lower(text)
    text = lemmatize(text)
    text = clean_white_space(text)

    return text


def downloadNLTK():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/wordnet.zip')
        nltk.data.find('corpora/omw-1.4.zip')
    except KeyError:
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('omw-1.4')


def remove_html_tags(text):
    """
    take string input and clean string without tags.
    use regex to remove the html tags.
    """
    return re.sub('<[^<]+?>', '', text)


def remove_leetspeak(text):
    return re.sub(r"[A-Za-z]+\d+|\d+[A-Za-z]+|[A-Za-z]+\d+[A-Za-z]+",'',text).strip()


def replace_contractions(text):
    expanded_words = []
    for word in text.split():
        expanded_words.append(contractions.fix(word))

    return ' '.join(expanded_words)


def replace_atUser(text):
    text = re.sub('@[^\s]+', 'atUser', text)
    return text


def replace_url(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'url', text)
    text = re.sub(r'#([^\s]+)', r'\1', text)
    return text


def remove_numbers(text):
    text = ''.join([i for i in text if not i.isdigit()])
    return text


def to_lower(text):
    return text.lower()


def remove_punct(text):
    return ''.join(c for c in text if c not in punctuation)


def stem(text):
    stemmer = SnowballStemmer('english')

    stemmed_word = [stemmer.stem(word) for sent in nltk.sent_tokenize(text) for word in
                    nltk.word_tokenize(sent)]
    return " ".join(stemmed_word)


def lemmatize(text):
    lemmatizer = WordNetLemmatizer()

    lemmatized_word = [lemmatizer.lemmatize(word) for sent in nltk.sent_tokenize(text) for word in
                       nltk.word_tokenize(sent)]
    return " ".join(lemmatized_word)


def remove_smiley(text):
    # https://de.wiktionary.org/wiki/Verzeichnis:International/Smileys

    SMILEYS = {
        ":)": "",
        ":-)": "",
        ":^)": "",
        ":-]": "",
        "=]": "",
        ":]": "",
        ":D": "",
        ":-D": "",
        ":))": "",
        ";-)": "",
        ";-]": "",
        ";o)": "",
        "¦)": "",
        "=:)": "",
        ":3": "",
        ":9": "",
        "c:": "",
        ":'D": "",
        "xD": "",
        "XD": "",
        "B)": "",
        "B-)": "",
        "8)": "",
        "8-)": "",
        "=8)": "",
        "=8^)": "",
        "=B)": "",
        "=B^)": "",
        "~8D": "",
        "y=)": "",
        ">:)": "",
        ">:D": "",
        ">:>": "",
        ">:[]": "",
        "^_^": "",
        "^-^": "",
        "^.^": "",
        "^,^": "",
        "^^": "",
        "^^": "",
        "^^'": "",
        "^^°": "",
        "^////^": "",
        "^o^": "",
        "^O^": "",
        "^0^": "",
        "\o/": "",
        "<o/": "",
        "<(^.^)>": "",
        "-^_^-": "",
        "*(^_^)*": "",
        "*0*": "",
        "Ü": "",
        "*~*": "",
        ":>": "",
        ":i": "",
        "l:": "",
        ":(": "",
        ":c": "",
        ":[": "",
        "=(": "",
        "=[": "",
        ":'(": "",
        ":,(": "",
        ";(": "",
        ";_;": "",
        "T.T": "",
        "T_T": "",
        "Q_Q": "",
        ":S": "",
        ":-/": "",
        ":/": "",
        ":-I": "",
        ">:(": "",
        ">:o": "",
        ">:O": "",
        ">:@": "",
        "D:": "",
        "DX": "",
        ":-E3": "",
        "x_X": "",
        "X_x": "",
        "x_x": "",
        "x.X": "",
        "X.x": "",
        "x.x": "",
        "°_°": "",
        ">.<": "",
        ">,<": "",
        "-.-": "",
        "-,-": "",
        "-_-": "",
        "._.": "",
        "^_°'": "",
        "^,°'": "",
        "Oo": "",
        "oO": "",
        "O.o'": "",
        "cO": "",
        "ô_o": "",
        "Ô_ô": "",
        "D:": "",
        "D8<": "",
        "O_O": "",
        "Ò_Ó": "",
        "U_U": "",
        "v_v": "",
        ":<": "",
        "°_°": "",
        "m(": "",
        "°^°": "",
        "(@_@)": "",
        ";.;": "",
        ";)": "",
        ";-)": "",
        "^.-": "",
        ":§": "",
        ";D": "",
        ";-D": "",
        ":P": "",
        ":p": "",
        "c[=": "",
        ":p~~~~~~": "",
        ":-*": "",
        ":*": "",
        ";*": "",
        ":-x": "",
        "C:": "",
        ":o": "",
        ":-o": "",
        ":O": "",
        "0:-)": "",
        "O:-)": "",
        "3:)": "",
        "3:D": "",
        "-.-zZz": "",
        "(o)_(o)": "",
        "($)_($)": "",
        "^_-": "",
        "//.o": "",
        "^w^": "",
        "=^_^=": "",
        "x3": "",
        "*_*": "",
        "#-)": "",
        "`*,...ò_Ó...,*´": "",
        ":-{}": "",
        ":ö": "",
        "û_û": "",
        "Ö_Ö": "",
        ":o)": "",
        "cB": "",
        "BD": "",
        "Y_": "",
        ":-€": "",
        ":3": "",
        "x'DD": "",
        "l/l": "",
        ":o)>": "",
        "(_8(I)": "",
        "//:=|": "",
        "<3": "",
        "</3": "",
        "<'3": "",
        "<°(((><": "",
        "<°{{{><": "",
        "<°++++<": "",
        ">)))°>": "",
        "o=(====>": "",
        "@>--}---": "",
        "@>-`-,--": "",
        "(_|::|_)": "",
        "c(_)": "",
        "[:|]": "",
        "(°oo°)": "",
        "(.)(.)": "",
        "( . Y . )": "",
        "( . )": "",
        "| . |": "",
        ").(": "",
        "(_i_)": "",
        "( Y )": "",
        "8===D": ""
    }
    text = text.split()
    reformed = [SMILEYS[word] if word in SMILEYS else word for word in text]
    return " ".join(reformed)


def replace_smiley(text):
    # https://de.wiktionary.org/wiki/Verzeichnis:International/Smileys

    SMILEYS = {
        ":)": " smile ",
        ":-)": " smile ",
        ":^)": "",
        ":-]": "",
        "=]": "",
        ":]": "",
        ":D": "",
        ":-D": "",
        ":))": "",
        ";-)": "",
        ";-]": "",
        ";o)": "",
        "¦)": "",
        "=:)": "",
        ":3": "",
        ":9": "",
        "c:": "",
        ":'D": "",
        "xD": "",
        "XD": "",
        "B)": "",
        "B-)": "",
        "8)": "",
        "8-)": "",
        "=8)": "",
        "=8^)": "",
        "=B)": "",
        "=B^)": "",
        "~8D": "",
        "y=)": "",
        ">:)": "",
        ">:D": "",
        ">:>": "",
        ">:[]": "",
        "^_^": "",
        "^-^": "",
        "^.^": "",
        "^,^": "",
        "^^": "",
        "^^": "",
        "^^'": "",
        "^^°": "",
        "^////^": "",
        "^o^": "",
        "^O^": "",
        "^0^": "",
        "\o/": "",
        "<o/": "",
        "<(^.^)>": "",
        "-^_^-": "",
        "*(^_^)*": "",
        "*0*": "",
        "Ü": "",
        "*~*": "",
        ":>": "",
        ":i": "",
        "l:": "",
        ":(": " sad ",
        ":c": " sad ",
        ":[": " sad ",
        "=(": " sad ",
        "=[": " sad ",
        ":'(": "",
        ":,(": "",
        ";(": "",
        ";_;": "",
        "T.T": "",
        "T_T": "",
        "Q_Q": "",
        ":S": "",
        ":-/": "",
        ":/": "",
        ":-I": "",
        ">:(": "",
        ">:o": "",
        ">:O": "",
        ">:@": "",
        "D:": "",
        "DX": "",
        ":-E3": "",
        "x_X": "",
        "X_x": "",
        "x_x": "",
        "x.X": "",
        "X.x": "",
        "x.x": "",
        "°_°": "",
        ">.<": "",
        ">,<": "",
        "-.-": "",
        "-,-": "",
        "-_-": "",
        "._.": "",
        "^_°'": "",
        "^,°'": "",
        "Oo": "",
        "oO": "",
        "O.o'": "",
        "cO": "",
        "ô_o": "",
        "Ô_ô": "",
        "D:": "",
        "D8<": "",
        "O_O": "",
        "Ò_Ó": "",
        "U_U": "",
        "v_v": "",
        ":<": "",
        "°_°": "",
        "m(": "",
        "°^°": "",
        "(@_@)": "",
        ";.;": "",
        ";)": " wink ",
        ";-)": " wink ",
        "^.-": " wink ",
        ":§": "",
        ";D": "",
        ";-D": "",
        ":P": "",
        ":p": "",
        "c[=": "",
        ":p~~~~~~": "",
        ":-*": " kiss ",
        ":*": " kiss ",
        ";*": "",
        ":-x": "",
        "C:": "",
        ":o": "",
        ":-o": "",
        ":O": "",
        "0:-)": "",
        "O:-)": "",
        "3:)": " devil ",
        "3:D": "",
        "-.-zZz": "",
        "(o)_(o)": "",
        "($)_($)": "",
        "^_-": "",
        "//.o": "",
        "^w^": "",
        "=^_^=": "",
        "x3": "",
        "*_*": "",
        "#-)": "",
        "`*,...ò_Ó...,*´": "",
        ":-{}": "",
        ":ö": "",
        "û_û": "",
        "Ö_Ö": "",
        ":o)": "",
        "cB": "",
        "BD": "",
        "Y_": "",
        ":-€": "",
        ":3": "",
        "x'DD": "",
        "l/l": "",
        ":o)>": "",
        "(_8(I)": " Homer Simpson ",
        "//:=|": " Hitler ",
        "<3": " heart ",
        "</3": " broken heart ",
        "<'3": " broken heart ",
        "<°(((><": "",
        "<°{{{><": "",
        "<°++++<": "",
        ">)))°>": "",
        "o=(====>": "",
        "@>--}---": "",
        "@>-`-,--": "",
        "(_|::|_)": "",
        "c(_)": "",
        "[:|]": "",
        "(°oo°)": "",
        "(.)(.)": "",
        "( . Y . )": "",
        "( . )": "",
        "| . |": "",
        ").(": "",
        "(_i_)": "",
        "( Y )": "",
        "8===D": " penis "
    }
    text = text.split()
    reformed = [SMILEYS[word] if word in SMILEYS else word for word in text]
    return " ".join(reformed)


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
    text = re.sub('[\U0001F550-\U0001F567]', " of the clock ", text)

    text = emoji.demojize(text)
    text = text.replace(":", " ")
    return ' '.join(text.split())


def clean_white_space(text):
    return re.sub(' +', ' ', text)
