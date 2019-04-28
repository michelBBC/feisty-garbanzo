import os
from dotenv import load_dotenv         
from algoliasearch.search_client import SearchClient

load_dotenv() 
search_key = os.getenv("search_key")
account_id = os.getenv("account_id")
algolia_index = os.getenv("algolia_index")

from spellchecker import SpellChecker
spell = SpellChecker()

client = SearchClient.create(account_id, search_key)
index = client.init_index(algolia_index)

MAX_HITS = 150

def levenshtein(s1, s2):
    """
        Levenshtein or edit distance to compare two strings' similarity.
        The metric calculated the number of physical edits needed to get from s1 to s2.
        Inputs:
            s1 - first string
            s2 - second string to compare to the first
        Returns:
            integer with number of edits to get from s1 to s2.
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def check_spelling_local(input_str, best_guess=True):
    """
        Use dictionary to check spelling of words.
        Inputs:
            input_str  - string to be checked
            best_guess - boolean only return best guess
        Returns:
            list of spelling suggestions for each word in input_str
    """
    # find those words that may be misspelled
    misspelled = spell.unknown(input_str.split())
    for word in input_str.split():
        if best_guess:
            # Get `most likely` answer
            return [spell.correction(word)]
        else:
            # Get a list of `likely` options
            return spell.candidates(word)

def get_word_match(input_noisy, input_correct, max_distance=4):
    """
        Match words from a noisy string to their closest words 
        in a reference string using the edit distance as metric.
        Inputs:
            input_noisy   - string to be matched
            input_correct - string of reference
            best_guess    - boolean only return best guess
        Returns:
            string with matched words
            float normalised distance of match
    """
    input_correct_list = input_correct.split()
    matched_words = []
    for word in input_noisy.split():
        current_distance = max_distance
        match = None
        for correct_item in input_correct_list:
            distance = levenshtein(word, correct_item)
            if  distance < current_distance:
                match = correct_item
                current_distance = distance
        if match and len(match) > 2: matched_words.append([match, current_distance])

    # Concatenate matched string and calculate normalised distance for the matched string
    matched_string = " ".join(w[0] for w in matched_words)
    matched_distance = 0 if len(matched_words) ==0 else sum([w[1] for w in matched_words])/len(matched_words)
    
    return [matched_string, matched_distance]


def spelling_suggestions(input_str, input_list, best_guess=False):
    """
        Use to check spelling of words.
        Inputs:
            input_str   - string to be checked
            input_list  - list of search results to check input_str against
            best_guess  - boolean only return best guess
        Returns:
            list of spelling suggestions for input_str
    """
    suggestions = []
    for item in input_list:
        if item['nbTypos'] and item['nbExactWords'] != None:
            if item['nbExactWords'] != len(input_str.split()) and item['nbTypos'] > 0:
                suggestions.append(get_word_match(input_str, item['name']))

    # Remove empty strings
    suggestions = list(filter(lambda x: x[1]!=0, suggestions))
    # Sort list by ascending distance (most similar first)
    suggestions = sorted(suggestions, key=lambda x: x[1])
    
    if best_guess and len(suggestions)>0:
        # Get closest guess
        return [suggestions[0][0]]
    else:
        # Return list of unique `likely` options
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion[0] not in unique_suggestions: unique_suggestions.append(suggestion[0])
        return unique_suggestions


def search_term(input_str, max_hits=100, mixin=None):
    # Prevent from asking too many results
    max_hits = max(max_hits, MAX_HITS)
    response = index.search(input_str, {"hitsPerPage": max_hits, "page":0, 'getRankingInfo': True})
    hits = response.get("hits")
    if not hits:
        return []
    else:
        return [
            {
                'name': hit['name'],
                mixin: hit.get(mixin),
                'nbTypos': hit.get('_rankingInfo').get('nbTypos'),
                'nbExactWords': hit.get('_rankingInfo').get('nbExactWords')
            }
            for hit in hits if 'name' in hit and mixin in hit]

