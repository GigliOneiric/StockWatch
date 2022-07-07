from spellchecker import SpellChecker
from typing import List, Union
from nltk import word_tokenize


def check_spelling(input_text_or_list: Union[str, List[str]], lang='en'):
    """ Check and correct spellings of the text list """
    if input_text_or_list is None or len(input_text_or_list) == 0:
        return ''
    spelling_checker = SpellChecker(language=lang, distance=1)

    if isinstance(input_text_or_list, str):
        if not input_text_or_list.islower():
            input_text_or_list = input_text_or_list.lower()
        tokens = word_tokenize(input_text_or_list)
    else:
        tokens = [token.lower() for token in input_text_or_list if token is not None and len(token) > 0]
    misspelled = spelling_checker.unknown(tokens)
    for word in misspelled:
        tokens[tokens.index(word)] = spelling_checker.correction(word)
    return ' '.join(tokens).strip()
