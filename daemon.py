""" Constructs the Flask instance and any extensions. """

from flask import Blueprint
from flask.ext.restful import Api
from flask.ext.pymongo import PyMongo

app = Blueprint('tactical', __name__)

from config import *

api = Api(app)
mongo = PyMongo(app)
