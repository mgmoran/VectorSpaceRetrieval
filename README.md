**Description:** This module builds and runs a vector-space model information retrieval system
on a database of 2019 films scraped from Wikipedia. The search engine queries over combined Title
and Text fields of the database entries, and supports a "More Like This" functionality, which retrieves
documents with similarity scores to the query that are sufficiently close to the document in question.

### Build Instructions
* Run pre_process.py to build and shelve the index files. Outputs 5 shelf files:
    * 2019_db.db : Postings list, mapping doc ID numbers to document entries.
    * inverted_index.db : Inverted Index, mapping vocabulary terms to documents and corresponding term frequencies
    * idf_index.db : IDF index, mapping vocabulary terms to their IDF values
    * vocabulary.db : Stored vocabulary compiled from the database
    * doc_lengths.db : Index mapping document IDs to their cosine-normalized length
* Expected build time: 1.0 minutes, 8.10 s

### Run instructions
* Run hw3.py to launch the application for searching.
* Expected retrieval time: ~ 9.52 s

### Modules:
* Pre_process.py: builds and shelves all index files necessary for retrieval
* hw3.py: runs a flask app that serves as the interface to a vector
space information retrieval model.
* utils.py: Home of all helper methods used to implement the vector-space model of retrieval, including:
    * normalizing text: case-folding, stemming (using nltk's PorterStemmer) removal of stopwords, etc.
    * tf-idf weighting query and document terms
    * computing cosine similarity of query and documents
    * ranking results by similarity scores
    * retrieving structured information for presentation on results page

