from flask import Flask, request
from flask.wrappers import Response

import json

from .utils import *

json_headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    """ Ping (alive test) endpoint. """
    return Response("Hello", 200)


@app.route("/search", methods=["GET", "POST"])
def search_items():
    """
    Search for products by name.
    """
    if request.method == "POST":
        # Post request
        payload = request.get_json(silent=True)
        if not payload:
            # Bad payload, return with user error
            return Response("Missing or ill-formatted query. For POST requests, payload of format {'query': '<word>'} is required as well as correct headers ('Content-Type': 'application/json').", 400)
        query = payload.get("query")
        mixin = payload.get("mixin")
        max_hits = payload.get("max")
    else:
        # Get request
        query = request.args.get('q') or request.args.get('query')
        mixin = request.args.get("mixin")
        max_hits = request.args.get("max")
    if not query: 
        return Response("Empty query", 204)
    spell_check = False
    if spell_check:
        query = " ".join(w for w in check_spelling(query))
    max_h = max_hits or 10
    search_response = search_term(query, max_hits=max_h, mixin=mixin)
    return Response(json.dumps(search_response), 200, headers=json_headers)


@app.route("/correct", methods=["GET", "POST"])
def correct_items():
    if request.method == "POST":
        # Post request
        payload = request.get_json(silent=True)
        if not payload:
            # Bad payload, return with user error
            return Response("Missing or ill-formatted query. For POST requests, payload of format {'query': 'word'} is expected as well as correct headers for Content-Type.", 400)
        query = payload.get("query")
    else:
        # Get request
        query = request.args.get('q') or request.args.get('query')
    if not query: 
        return Response("Empty input", 204)
    corrected = [w for w in check_spelling(query)]
    return Response(json.dumps(corrected), 200, headers=json_headers)


if __name__ == "__main__":
    app.running_update = True
    http_server = app.run(host="0.0.0.0", port=8080, debug=True)