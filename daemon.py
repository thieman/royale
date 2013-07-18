""" Constructs the Flask instance and any extensions. """

from flask import Flask
from flask.ext.restful import Api
from flask.ext.pymongo import PyMongo

app = Flask('royale')
api = Api(app)
app.config['MONGO_HOST'] = 'ec2-107-21-83-199.compute-1.amazonaws.com'
app.config['MONGO_PORT'] = 27018
mongo = PyMongo(app)
