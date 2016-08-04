import unittest
from search import search
from build_index import readIndexFromFile


index = readIndexFromFile()


class SearchTest(unittest.TestCase):

    def test_1gram(self):
        results = search('happy', index)
        self.assertDictEqual(results, {'happy': {2012}})

