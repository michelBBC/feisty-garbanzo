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
            },
            {
                "name":	"Metra - 4AWG Complete Amp Kit",
                "image": "https://cdn-demo.algolia.com/bestbuy/1678623_sb.jpg",
                "nbTypos":	1,
                "nbExactWords": 0
            }
        ]
        suggestions = ["Amazon", "Amp"]
        best_suggestion = [suggestions[0]]
        self.assertEqual(
            spelling_suggestions(word, input_list), suggestions
        )
        self.assertEqual(
            spelling_suggestions(word, input_list, True), best_suggestion
        )


    def test_get_word_match(self):
        match_target = "Amazon - Fire TV Stick"

        query = "Amazn"
        self.assertEqual(get_word_match(query, match_target)[0], "Amazon")

        query2 = 'Amazn styck'
        self.assertEqual(get_word_match(query2, match_target)[0], "Amazon Stick")

        match_target2 = "Amazon - Fire Wireless Bluetooth Game Controller - Black"
        self.assertEqual(get_word_match(query2, match_target2)[0], "Amazon Black")
