""" Constructs the Flask instance and any extensions. """

from flask import Flask
from flask.ext.restful import Api
from flask.ext.pymongo import PyMongo

app = Flask('royale')
api = Api(app)
mongo = PyMongo(app)
