"""
This module pre-processes a corpus of Wikipedia movie pages for indexing and querying.
Using an existing JSON corpus of movie documents, it extracts a normalized vocabulary from
the corpus and creates an inverted index using this vocabulary.

Vocabulary is normalized using a regex word-tokenizer and NLTK's built-in Porter Stemmer.
NLTK's list of stopwords is stemmed and stored so that incoming queries can be checked
against it.

"""

import json
import re
import math
import shelve
from utils import *
from collections import defaultdict
import logging

inverted_index = defaultdict(lambda: defaultdict(int))

def shelve_corpus(corpus,test):
    """
    - Open up the JSON corpus and shelve it
    - Normalize the text of each document and build a vocabulary
    - Create and shelve an inverted index of terms

    :param corpus: a JSON-format corpus of movies
    :return: None
    """
    logging.info("building inverted index...")
    with open(corpus, 'r') as json_corpus, shelve.open('2019_db', 'n') as database:
        movies = json.load(json_corpus)
        if test==True:
            movies = {k:v for k,v in movies.items() if int(k)<10}
        all_doc_ids = movies.keys()
        num_movies = len(all_doc_ids)
        database.update(movies)
        for doc_id in movies:
            vocab = Counter(normalize(movies[doc_id]['Title'] + " " + movies[doc_id]['Text']))
            for term in vocab:
                inverted_index[term][doc_id] = vocab[term]

        ### want to us ea tuple of term, IDF as keys, but shelve won't allow, only allows string keys
        ### instead do multiple shelve objects. one links terms to IDF, another links terms to Docs and DFs
        with shelve.open('inverted_index','n') as inverted:
            inverted.update(inverted_index)

        logging.info("building idf index...")
        idf_index = {term: calculate_idf(len(inverted_index[term]), num_movies) for term in inverted_index}
        with shelve.open('idf_index', 'n') as idf:
            idf.update(idf_index)

        logging.info("building doc_length index...")
        ### constructing document length index
        with shelve.open('doc_lengths','n') as f:
            for doc_id in all_doc_ids:
                text = set(normalize(movies[doc_id]['Title'] + " " + movies[doc_id]['Text']))
                normalized_length = math.sqrt(sum([weight_doc_term(inverted_index, term, doc_id)**2 for term in text]))
                f.update({doc_id: normalized_length})

@timer
def build(test=False):
    """
    Shelves an existing corpus of Wikipedia movie pages, and updates the global
    variable "vocab" with the vocabulary compiled from the corpus.

    :param test: whether or not to build an index from the test corpus.
    :return: None
    """
    shelve_corpus('[Molly Moran]_corpus.json', test)

if __name__=='__main__':
    build()