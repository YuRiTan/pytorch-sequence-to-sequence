import numpy as np


class Language:
    """ Utility class that serves as a language dictionary """
    def __init__(self, name):
        self.name = name
        # Count how often a word occurs in the language data.
        self.word2count = {}
        # Words are mapped to indices and vice versa
        self.index2word = {0: "SOS", 1: "EOS"}
        self.word2index = {v:k for k, v in self.index2word.items()}
        # Total word count
        self.n_words = 2  # Count SOS and EOS

    def add_sentence(self, sentence):
        """ Process words in a sentence string. """
        for word in sentence.split(' '):
            self.add_word(word)

    def add_word(self, word):
        """ Process a word (e.g. put it in vocabulary and count) """
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        elif word != 'SOS' and word != 'EOS':
            self.word2count[word] += 1
    
    def translate_indexes(self, idx):
        """ Takes in a vector of indices and returns the sentence. """
        return [self.index2word[i] for i in idx]
    
    def translate_words(self, words):
        """ Takes in a vector of indices and returns the sentence. """
        return [self.word2index[w] for w in words.split(' ')]
    
    
class Data:
    """Utility class that helps shuffle & query sentences later on."""
    def __init__(self, pairs, lang_1, lang_2):
        self.pairs = np.array(pairs)        
        self.shuffle_idx = np.arange(len(pairs))
        self.idx_pairs = self._get_idx_pairs(lang_1, lang_2)
                
    def __str__(self):
        return self.pairs
    
    def _get_idx_pairs(self, lang_1, lang_2):
        idx_1 = [
            [lang_1.word2index[word] for word in s.split(' ')] 
            for s in self.pairs[:, 0]
        ]
        idx_2 = [
            [lang_2.word2index[word] for word in s.split(' ')]
            for s in self.pairs[:, 1]
        ]
        return np.array(list(zip(idx_1, idx_2)), dtype=object)
    
    def shuffle(self):
        np.random.shuffle(self.shuffle_idx)
        self.pairs = self.pairs[self.shuffle_idx]
        self.idx_pairs = self.idx_pairs[self.shuffle_idx]    
