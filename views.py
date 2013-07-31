""" Royale views for rendering and data access """

from flask import render_template

def index_route(blueprint_name=None):
    return render_template('/'.join([blueprint_name, 'index.html']),
                           blueprint_name=blueprint_name)

def register_views(bp):
    defaults = {'blueprint_name': bp.name}
    bp.add_url_rule('/', 'index', index_route, defaults=defaults)
