import re
import unicodedata

from utils import Language, Data


def unicode2ascii(s):
    """Turn a Unicode string to plain ASCII, thanks to:
    http://stackoverflow.com/a/518232/2809427
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def normalize_string(s):
    """Lowercase, trim, and remove non-letter characters."""
    s = unicode2ascii(s.lower().strip())
    s = re.sub(r"\s?[.!?]", r" EOS", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s


def read_lang_pairs(lang1, lang2):
    print("Reading lines...")
    # Read the file and split into lines
    with open(f'data/{lang1}-{lang2}.txt', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    # Split every line into pairs and normalize
    pairs = [[normalize_string(s) for s in l.split('\t')] for l in lines]

    return pairs


def filter_pairs_eng2other(pairs):
    """Filters out more simple examples for English to French translation."""
    max_length = 10
    eng_prefixes = ("i am ", "i m ",
                    "he is", "he s ",
                    "she is", "she s",
                    "you are", "you re ",
                    "we are", "we re ",
                    "they are", "they re ")
    
    def keep_pair(p):
        short_sentence_eng = len(p[0].split(' ')) < max_length
        short_sentence_fra = len(p[1].split(' ')) < max_length
        simple_sentence = p[0].startswith(eng_prefixes)
        keep = short_sentence_eng and short_sentence_fra and simple_sentence
        return keep
    
    return [p for p in pairs if keep_pair(p)]
