""" Constructs the Flask instance and any extensions. """

from flask import Blueprint
from flask.ext.restful import Api
from flask.ext.pymongo import PyMongo

from resources import register_resources
from views import register_views

class RoyaleBlueprintFactory():

    def new(self, name, pymongo_instance):

        bp = Blueprint(name, __name__)

        bp.handle_exception = None
        bp.handle_user_exception = None

        api = Api(bp)
        mongo = pymongo_instance

        register_resources(api, mongo)
        register_views(bp)

        return bp
