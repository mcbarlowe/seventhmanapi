'''Creating Flask application factory'''

from flask import Flask
from models import db


# application factory
def create_app():
    '''create flask app'''
    # create application instance
    app = Flask(__name__)
    db.init_app(app)

    return app
