import os
import glob
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import wordpunct_tokenize


class InvertedIndex(defaultdict):

    def __init__(self):
        defaultdict.__init__(self, list)
        self._books = set()

    def merge(self, dict2):
        for token, posting in dict2.iteritems():
            self[token].append(posting)
            self._books |= set(posting[0])

    def updateBooks(self):
        for posting in self.values():
            self._books |= set([post[0] for post in posting])

    @property
    def books(self):
        return self._books


def getPaths():
    return glob.glob('*/*.txt')


def buildBookIndex(pathname):

    f = open(pathname, 'rb')
    bookId = pathname[:-4]

    tokenizer = wordpunct_tokenize
    stemmer = PorterStemmer()
    index = dict()
    pos = 0

    for line in f:
        for i, token in enumerate(tokenizer(line.strip().lower().decode('utf-8'))):
            token = stemmer.stem(token)
            if token not in index:
                index[token] = [bookId, [str(pos + i)]]
            else:
                index[token][-1].append(str(pos + i))
        pos += i + 1

    f.close()
    return index


def buildMainIndex():

    index = InvertedIndex()

    for book in getPaths():
        index.merge(buildBookIndex(book))

    return index


def updateMainIndex():

    from_scratch = False

    if os.path.isfile('inverted_index.txt'):
        index = readIndexFromFile()
    else:
        index = buildMainIndex()
        from_scratch = True

    if not from_scratch:
        for book in getPaths():
            if book not in index.books:
                index.merge(buildBookIndex(book))

    return index


def writeIndexToFile(index):

    with open('inverted_index.txt', 'wb') as f:
        for token, postings in index.iteritems():
            line = token + '||' + ';'.join(['{}:{}'.format(book, ','.join(posting))
                                            for book, posting in postings])
            f.write(line.encode('utf-8') + '\n')

    return True


def readIndexFromFile():

    index = InvertedIndex()

    with open('inverted_index.txt', 'rb') as f:
        for line in f:
            token, postings = line.decode('utf-8').strip().split('||')
            postings = [[book, locs.split(',')] for book, locs in
                        [posting.split(':') for posting in postings.split(';')]]
            index[token] = postings

    index.updateBooks()
    return index

