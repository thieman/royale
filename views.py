""" Royale views for rendering and data access """

from flask import render_template

from daemon import app

@app.route('/', methods=['GET'])
def index_route():
    return render_template('index.html')
