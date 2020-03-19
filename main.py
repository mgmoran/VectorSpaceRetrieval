"""
This module provides the user interface to a vector-space model search engine. The search engine
queries over a database of Wikipedia pages corresponding to movies released in 2019.

"""

from flask import Flask, render_template, request
from utils import *
from build_index import vocab
import shelve
from collections import defaultdict


# Create an instance of the flask application within the appropriate namespace (__name__).
# By default, the application will be listening for requests on port 5000 and assuming the base 
# directory for the resource is the directory where this module resides.
app = Flask(__name__)


# Welcome page
@app.route("/")
def query():
    """For top level route ("/"), simply present a query page."""
    return render_template('query_page.html')

@app.route("/results", methods=['POST'])
def results():
    """Normalizes the raw query and uses it to generate a result set.

    Presents the first 10 results starting with <page_num>."""
    page_num = int(request.form['page_num'])

    # Gathering all raw user queries from all fields
    query = request.form['query']

    # calculate and remove unknown terms
    index = shelve.open('inverted_index','r')
    vocab = index.keys()
    normalized_query = normalize(query)
    unknown_terms = [term for term in normalized_query if term not in vocab]

    # gathering stopwords
    skipped = [term for term in normalized_query if term in stops]

    # removing them
    valid_query = [term for term in normalized_query if term in vocab and term not in stops]
    index.close()

    # If after normalization, query is empty, render the error page.
    if valid_query==[]:
        return render_template('error_page.html')
    
    else:
        movie_ids = search(valid_query)

        num_hits = len(movie_ids)  # Save the number of hits to display later
        movie_ids = movie_ids[((page_num - 1) * 10):(page_num * 10)]  # Limit of 10 results per page
        movie_results = [movie_snippet(e) for e in movie_ids]

        return render_template('results_page.html', orig_query=query, movie_results=movie_results, srpn=page_num,
                               len=len(movie_ids), skipped_words=skipped, unknown_terms=unknown_terms,
                               total_hits=num_hits)

# Process requests for movie_data pages
# This decorator uses a parameter in the url to indicate the doc_id of the film to be displayed
@app.route('/movie_data/<film_id>')
def movie_data(film_id):
    """Given the doc_id for a film, present the title and text (optionally structured fields as well)
    for the movie."""
    data = get_movie_data(film_id)  # Get all of the info for a single movie
    return render_template('doc_data_page.html', data=data)


# If this module is called in the main namespace, invoke app.run().
# This starts the local web service that will be listening for requests on port 5000.
if __name__ == "__main__":
    app.run(debug=True)
