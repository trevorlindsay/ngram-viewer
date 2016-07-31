import os


def getFilePaths():

    paths = {}
    for year in [2012, 2013, 2014, 2015, 2016]:
        paths[year] = [file for file in os.listdir(`year`) if '.txt' in file]

    return paths


def stream(f, year, ngrams, ngram_count):

    # Keep track of the length of longest ngram (n)
    # When moving between lines, only need to remember
    # last n items from previous line
    longest = max([len(ngrams.split(','))])
    curr = ""

    for line in f:

        # Add line to search string
        curr += line.strip().lower()

        for ngram in ngrams.split(','):
            if ngram in curr:
                ngram_count[ngram][year] += 1

        # Only remember, at most, the last n words
        curr = " ".join(curr.split()[-longest:])

    return ngram_count


def search(ngrams):

    # If 'Graph!' button was hit with nothing in box
    if ngrams == '':
        return None

    # Just in case spaces and commas were used to separate ngrams
    ngrams = ngrams.replace(', ', ',').encode('utf-8').lower()

    ngram_count = {ngram: {year: 0 for year in [2012,2013,2014,2015,2016]} for ngram in ngrams.split(',')}
    filepaths = getFilePaths()

    # Iterate over every book
    for year in filepaths.keys():
        for file in filepaths[year]:
            with open('{}/{}'.format(year, file), 'rb') as f:
                ngram_count = stream(f, year, ngrams, ngram_count)

    return ngram_count
