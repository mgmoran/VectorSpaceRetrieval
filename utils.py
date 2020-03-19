"""
This module contains various functions that facilitate querying over an index and displaying
information from the index.

"""
import functools
import itertools
import re
import math
import shelve
import time
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem.porter import *
from collections import defaultdict, Counter
import logging

from nltk.tokenize import sent_tokenize

word_tokenize = re.compile(r'\b[\w]\S*[\w]\b')
porter_stemmer = PorterStemmer()
stops = [porter_stemmer.stem(token) for token in set(stopwords.words('english'))]

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_t = time.perf_counter()
        f_value = func(*args, **kwargs)
        elapsed_t = time.perf_counter() - start_t
        mins = elapsed_t // 60
        print(f'Elapsed time: {mins} minutes, {elapsed_t - mins * 60:0.2f} seconds')
        return f_value

    return wrapper_timer

@timer
def search(query):
    """
    Takes the input from all query fields and searches the database for matching
    documents.

    :param queries: a list of four separate queries corresponding two the four input fields
    on the query page
    :return: a list of document IDs matching all non-null queries
    """
    ### field accessors for get_movie_data

    with shelve.open('inverted_index', 'r') as f, shelve.open('idf_index', 'r') as g, shelve.open('doc_lengths',
                                                                                                  'r') as z, shelve.open(
        '2019_db') as x:
        docs = [f[term] for term in query]
        results = list(set.union(*[set(films) for films in docs]))
        similarity_scores = defaultdict(float)
        logging.info("calculating similarity scores...")
        for doc in results:
            weighted_query = weight_query(query, f, g, doc)
            normalized_doc_length = z[doc]
            doc_text = x[doc]['Title'] + " " + x[doc]['Text']
            doc_terms = [token for token in normalize(doc_text) if token in query]
            weighted_doc = weight_doc(doc, normalized_doc_length, doc_terms, f)
            similarity_score = compute_similarity(weighted_query, weighted_doc)
            similarity_scores[doc] = similarity_score
        ranked = sorted(similarity_scores.keys(), key= lambda x: similarity_scores[x], reverse=True)
        return ranked


def get_movie_data(doc_id):
    """
    Return data fields for a movie.

    :param doc_id: ID corresponding to a document in the database.
    :return: a 5-tuple with structured field information corresponding to the document
    """
    with shelve.open('2019_db', 'r') as f:
        title = f[doc_id]['Title']
        director = f[doc_id]["Director"]
        country = f[doc_id]["Country"]
        starring = f[doc_id]["Starring"]
        # splitting text into paragraphs for ease of display on the doc_data page.
        text = f[doc_id]["Text"].split("\n")
        return title, director, country, starring, text


def movie_snippet(doc_id):
    """
     Builds a "snippet" of text for the results page, using the first 3 sentences of the
    'Text' field of a document.

    :param doc_id: ID corresponding to a document in the index
    :return: a tuple, consisting of the doc ID, its title and the snippet
    """
    with shelve.open('2019_db', 'r') as f:
        title = f[doc_id]['Title']
        sents = sent_tokenize(f[doc_id]['Text'])
        snippet = ' '.join(sents[:3])
        return doc_id, title, snippet

def compute_similarity(query, doc):
    return sum([query[term] * doc[term] for term in doc])

def weight_query(query, inverted_index, idf_index, doc):
    weighted_query = defaultdict(float)
    for term in set(query):
        tf = query.count(term) ### is this right??
        idf = idf_index[term]
        if tf !=0:
            term_weight = (1 + math.log10(tf)) * idf  ## already logged and inverted in the index
        else:
            term_weight = 0
        weighted_query[term] = term_weight
    return weighted_query

def weight_doc(doc, doc_length, doc_terms, inverted_index):
    """

    :param doc:
    :param doc_length:
    :param doc_terms:
    :param inverted_index:
    :return:
    """
    weighted_doc = defaultdict(float)
    for term in set(doc_terms):
        term_weight = weight_doc_term(inverted_index, term, doc)
        normalized = term_weight / doc_length
        weighted_doc[term] = normalized
    return weighted_doc

def weight_doc_term(inverted_index, term, doc):
    """

    :param inverted_index:
    :param term:
    :param doc:
    :return:
    """
    tf = inverted_index[term][doc]
    term_weight = (1 + math.log10(tf))
    return term_weight

def calculate_idf(length, num_movies):
    """

    :param length:
    :param num_movies:
    :return:
    """
    return math.log10(num_movies / length)

def normalize(text):
    """
    The string is first tokenized using a regex tokenizer, which separates on space and punctuation
    at word boundaries. The remaining tokens are then stemmed using nltk's Porter Stemmer.

    :param text: a string
    :param stemmed: a boolean corresponding to whether or not the input should be stemmed
    :return: a list, corresponding to a tokenized and stemmed version of the input stirng
    """
    basic_tokenize = [token.lower() for token in re.findall(word_tokenize,text)]
    normalized =[porter_stemmer.stem(token) for token in basic_tokenize]
    return normalized

