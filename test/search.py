import os


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
    books = set()

    for ngram in ngrams:

        books = set()

        for word in ngram.split():

            try:
                books |= set([posting[0] for posting in index[word]])
            except:
                pass

        for book in books:

            year = int(book.split('/')[0])
            locs = []

            for word in ngram.split():
                locs += [posting[1] for posting in index[word] if posting[0] == book]

            locs = [set([int(pos) - i for pos in loc]) for i, loc in enumerate(locs)]
            ngram_count[ngram][year] += len(set.intersection(*locs))

    return ngram_count
