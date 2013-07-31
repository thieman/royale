""" Royale views for rendering and data access """

from flask import render_template

def index_route():
    return render_template('index.html')

def register_views(bp):
    bp.add_url_rule('/', 'index', index_route)
