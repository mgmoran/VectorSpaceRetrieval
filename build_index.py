from utils import *
from pre_process import stops, shelve_corpus, normalize
import shelve
from collections import defaultdict
global vocab
vocab = set()

def build(test=False):
    """
    Shelves an existing corpus of Wikipedia movie pages, and updates the global
    variable "vocab" with the vocabulary compiled from the corpus.

    :param test: whether or not to build an index from the test corpus.
    :return: None
    """
    timer(shelve_corpus('[Molly Moran]_corpus.json', test))
    with shelve.open('inverted_index', 'r') as f:
        vocab.update(f.keys())

if __name__=='__main__':
    build()