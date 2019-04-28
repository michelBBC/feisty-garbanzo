from flask import Flask, request
from flask_selfdoc import Autodoc
from flask.wrappers import Response

import json
import os

from .utils import *

json_headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}

app = Flask(__name__)
auto = Autodoc(app)

api_version = os.getenv('api_version')

@app.route('/', methods=['GET'])
def help():
    """ Display help. """
    # return auto.html()
    return auto.html(title='Search with spellchecker API: endpoints', template="autodoc_custom.html")

@app.route("/ping", methods=["GET"])
@auto.doc()
def hello():
    """
    Ping (alive test).
    """
    return Response("Hello", 200)


@app.route("/suggestions", methods=["GET", "POST"])
@auto.doc()
def suggest_items():
    """
    Get spelling suggestions for a given search term.
    """
    if request.method == "POST":
        # Post request
        payload = request.get_json(silent=True)
        if not payload:
            # Bad payload, return with user error
            return Response("Missing or ill-formatted query. For POST requests, payload of format {'query': '<word>'} and correct headers ('Content-Type': 'application/json') are required.", 400)
    else:
        # Get request
        payload = request.args

    # Get parameters of request
    query = payload.get("query") or payload.get("q")
    mixin = payload.get("mixin")
    max_hits = payload.get("max")
    include_products = payload.get("products") == 'true' if "products" in payload else False
    if not query: 
        return Response("Empty query", 204)

    # Get search results
    max_h = max_hits or 10
    search_response = search_term(query, max_hits=max_h, mixin=mixin)

    # Do spelling check
    # suggestions = []
    suggestions = spelling_suggestions(query, search_response, best_guess=False)

    # Format response
    if include_products:
        response = {'results': search_response, 'spelling_suggestions': suggestions, 'spelling_correct': len(suggestions)==0}
    else:
        response = {'spelling_suggestions': suggestions}

    response['metadata'] = {'request': request.url, 'version': api_version}
    return Response(json.dumps(response), 200, headers=json_headers)