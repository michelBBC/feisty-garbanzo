import os
from dotenv import load_dotenv         
from algoliasearch.search_client import SearchClient

load_dotenv() 
search_key = os.getenv("search_key")
account_id = os.getenv("account_id")
algolia_index = os.getenv("algolia_index")

client = SearchClient.create(account_id, search_key)
index = client.init_index(algolia_index)

from spellchecker import SpellChecker

spell = SpellChecker()

MAX_HITS = 150

def correct_spelling(input_str):
    misspelled = spell.unknown(input_str.split())
    corrected = []
    for word in input_str.split():
        if word in misspelled:
            word = spell.correction(misspelled.pop())
        corrected.append(word)

        return corrected

def check_spelling(input_str, best_guess=True):
    # find those words that may be misspelled
    misspelled = spell.unknown(input_str.split())
    for word in input_str.split():
        if best_guess:
            # Get the one `most likely` answer
            # print(spell.correction(word))
            return [spell.correction(word)]
        else:
            # Get a list of `likely` options
            # print(spell.candidates(word))
            return spell.candidates(word)


def search_term(input_str, max_hits=100, mixin=None):
    # Prevent from asking too many results
    max_hits = max(max_hits, MAX_HITS)
    response = index.search(input_str, {"hitsPerPage": max_hits, "page":0})
    hits = response.get("hits")
    if not hits: return []
    if mixin:
        return [[hit['name'], hit[mixin]] for hit in hits if 'name' in hit and mixin in hit]
    else:
        return [hit['name'] for hit in hits if 'name' in hit]

def get_suggestions(input_str):
    return dict()
