from flask import Flask
from .server import app

def create_app():
    # app = Flask(__name__)
    application = app

    return application
