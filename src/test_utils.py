import unittest
from unittest.mock import patch


from utils import (
    spelling_suggestions,
    check_spelling_local,
    search_term,
    levenshtein,
    get_word_match
)


class UtilsTestCase(unittest.TestCase):

    def test_levenshtein(self):
        word1 = "kitten"
        word2 = "kitchen"
        self.assertEqual(levenshtein(word1, word2), 2)


    def test_check_spelling_local(self):
        word = "Cheeze"
        self.assertEqual(check_spelling_local(word), ["cheese"])

    def test_spelling_suggestions(self):
        word = "Amazn"
        input_list = [
            {
                "name": "Amazon - Fire TV Stick",
                "image": "https://cdn-demo.algolia.com/bestbuy/9999119_sb.jpg",
                "nbTypos": 1,
                "nbExactWords": 2
            }
        ]
        suggestions = ["Amazon"]
        self.assertEqual(
            spelling_suggestions(word, input_list), suggestions
        )


    def test_get_word_match(self):
        match_target = "Amazon - Fire TV Stick"

        query = "Amazn"
        self.assertEqual(get_word_match(query, match_target)[0], "Amazon")

        query = 'Amazn styck'
        self.assertEqual(get_word_match(query, match_target)[0], "Amazon Stick")
