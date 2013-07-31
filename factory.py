""" Constructs the Flask instance and any extensions. """

from flask import Blueprint
from flask.ext.restful import Api
from flask.ext.pymongo import PyMongo

from resources import register_resources
from views import register_views

class RoyaleBlueprintFactory(object):

    def new(self, name, template_folder, static_folder,
            pymongo_instance):

        bp = Blueprint(name, __name__,
                       template_folder=template_folder,
                       static_folder=static_folder)

        bp.handle_exception = None
        bp.handle_user_exception = None

        api = Api(bp)
        mongo = pymongo_instance

        register_resources(api, mongo)
        register_views(bp)

        return bp
