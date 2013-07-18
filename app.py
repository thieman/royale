""" Glues the various daemon pieces together to avoid circular imports. """

from daemon import app
from resources import *
from views import *

app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3581)
