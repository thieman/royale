""" Constructs the Flask instance and any extensions. """

from flask import Flask
from flask.ext.restful import Api
from flask.ext.pymongo import PyMongo

app = Flask('royale')

from config import *

api = Api(app)
mongo = PyMongo(app)
