# Proxy API for Spellcheck/"Did you mean?" feature

This API is an API Proxy/middleware to prototype a spellcheck or suggested correction feature on top of a deployed [Algolia](https://www.algolia.com) product database.

This package is written in Python 3 (3.6) and uses the micro web framework [Flask](http://flask.pocoo.org/) in order to serve a RESTful API.

## Available scripts

`make run-local` Run the API locally in _development mode_.  The API runs on http://127.0.0.1:5000/

`make test` Run unit tests

`make install` Installs dependencies (see below)

## Install

Dependencies are specified in the `Pipfile` and `Pipfile.lock` files and managed with [Pipenv](https://pipenv.readthedocs.io/en/latest/).

## Deployment

For deployment on a cloud platform as a service, such as [Heroku](www.heroku.com), the `Procfile` specifies the command to be run to spawn the Flask API on the cloud platform.

## Available Endpoints

`/`  [GET]  
Display short documentation ofavailable API endpoints.  


`/ping` [GET]  
Basic alive/ping endpoint.  


`/suggestions` [GET, POST]  
Get spelling suggestions for a word/product in the database.

GET  
    Parameters:  
    - `query=<term>` The term to be searched for, eg. 'Fish' 
    - `products=<true|false>` _optional_ include list of products in response
    - `mixin=<images>` _optional_ return urls of images in results  
    - `max=<integer>` _optional_ maximum number of results to be returned

POST  
    Expects `Content-Type: application/json` request header.
```
{
    'query': <term>,
    'products': <true|false>,
    'mixin': 'images',
    'max': <integer>
}
```
Optional parameters are identical to the GET request, ie. `mixin`, `max`, and `suggestions` are _optional_.

Sample response:

```
{
  "results": [
    [
      "Amazon - Fire TV Stick",
      "https://cdn-demo.algolia.com/bestbuy/9999119_sb.jpg"
    ],
    [
      "Amazon - Kindle Paperwhite 3G - Black",
      "https://cdn-demo.algolia.com/bestbuy/9440019_sb.jpg"
    ]
  ],
  "correct_spelling": false,
  "spelling_suggestions": [
    "Amazon"
  ],
  "metadata": {
    "request": "/search?q=Amazon&mixin=image&suggestions=true",
    "version": "v1"
  }
}
