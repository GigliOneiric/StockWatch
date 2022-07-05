import re
from string import punctuation

import nltk
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer


def preprocess(text):
    downloadNLTK()

    text = replaceURL(text)
    text = replaceAtUser(text)
    text = removeNumbers(text)
    text = to_lower(text)
    text = lemmatize(text)
    text = remove_punct(text)

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


def replaceAtUser(text):
    text = re.sub('@[^\s]+', 'atUser', text)
    return text


def replaceURL(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'url', text)
    text = re.sub(r'#([^\s]+)', r'\1', text)
    return text


def removeNumbers(text):
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
