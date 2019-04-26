import unittest
from unittest.mock import patch


from utils import (
    correct_spelling,
    check_spelling,
    search_term,
    get_suggestions
)


class UtilsTestCase(unittest.TestCase):

    def test_correct_spelling(self):
        self.assertEqual(
            correct_spelling("Cheeze"), 'cheese')

    def test_check_spelling(self):
        word = "natural"
        self.assertEqual(check_spelling(word), "natural")

    # @patch('utils.s3_event_is_removal')
    # def test_search_term(self, test_s3_event_is_removal):
        # test_s3_event_is_removal.return_value = False
        # self.assertTrue(s3_event_is_publish({"eventName": "ObjectCreated:Put"}))
        # self.assertFalse(s3_event_is_publish({"eventName": "ObjectRemoved:Delete"}))

        # test_s3_event_is_removal.return_value = True
        # self.assertFalse(s3_event_is_publish({"eventName": "ObjectCreated:Put"}))

    def test_get_suggestions(self):
        word = "Amazn"
        suggestions = ["amazon", "amaze"]
        self.assertEqual(
            get_suggestions(word), suggestions
        )