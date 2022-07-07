# Implementation of removing stopwords using all stop words from nltk, spacy, gensim
import nltk
import spacy
import gensim
from nltk import word_tokenize
from nltk.corpus import stopwords


def downloadNLTK():
    try:
        nltk.data.find('corpora/stopwords')
    except KeyError:
        nltk.download('stopwords')


class StopWords:

    def __init__(self, text):
        downloadNLTK()

        self.text = text

        # list of stopwords from nltk
        stopwords_nltk = list(stopwords.words('english'))
        sp = spacy.load('en_core_web_sm')
        # list of stopwords from spacy
        stopwords_spacy = list(sp.Defaults.stop_words)
        # list of stopwords from gensim
        stopwords_gensim = list(gensim.parsing.preprocessing.STOPWORDS)

        # unique stopwords from all stopwords
        self.all_stopwords = []
        self.all_stopwords.extend(stopwords_nltk)
        self.all_stopwords.extend(stopwords_spacy)
        self.all_stopwords.extend(stopwords_gensim)
        # all unique stop words
        self.all_stopwords = list(set(self.all_stopwords))
        self.all_stopwords.remove('not')

    def remove_stopwords(self):

        text_without_sw = []
        # tokenization
        text_tokens = word_tokenize(self.text)
        for word in text_tokens:
            # checking word is stopword or not
            if word not in self.all_stopwords:
                text_without_sw.append(word)

        return ' '.join(text_without_sw)
