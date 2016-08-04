import os
from nltk.stem.porter import PorterStemmer


def search(ngrams, index):

    # If 'Graph!' button was hit with nothing in box
    if ngrams == '':
        return None

    # Just in case spaces and commas were used to separate ngrams
    ngrams = ngrams.replace(', ', ',').encode('utf-8').lower().split(',')

    years = []
    for dir in next(os.walk('.'))[1]:
        try:
            years.append(int(dir))
        except:
            pass

    ngram_count = {ngram: {year: 0 for year in years} for ngram in ngrams}
    stemmer = PorterStemmer()

    for ngram in ngrams:

        books = list()

        for word in ngram.split():

            # Get stem of word
            word = stemmer.stem(word)

            try:
                # Get set of books the word appears in
                books.append(set([posting[0] for posting in index[word]]))
            except:
                # If the word is not in the index
                pass

        # Get the set of books in which all words in the ngram appear
        books = set.intersection(*books) if len(books) > 0 else set()

        for book in books:

            year = int(book.split('/')[0])
            locs = []

            # For each book, get all of the locations of where the words in the ngram appear
            for word in ngram.split():
                word = stemmer.stem(word)
                locs.extend([posting[1] for posting in index[word] if posting[0] == book])

            # Check if the words are next to each other
            # e.g. ngram = 'run away from here' and the positions of the words are [[2,10] [3], [4,8,12,29], [5]]
            # This line of code will shift the position of each word over by its distance from the
            # beginning of the ngram to produce new positions [[2,10], [2], [2,6,10,29], [2]]
            # Then I take the intersection of these positions -- if it's not empty, then the ngram appears in the book
            locs = [set([int(pos) - i for pos in loc]) for i, loc in enumerate(locs)]
            ngram_count[ngram][year] += len(set.intersection(*locs))

    return ngram_count
