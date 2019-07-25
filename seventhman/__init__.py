'''Creating Flask application factory'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    '''Initialize the core application'''

    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config')

    # initialize pllugins
    db.init_app(app)

    with app.app_context():
# this has to go after the code above or else it cant import
# the db class to query the database
        from seventhman.stats.controllers import stats
        app.register_blueprint(stats)

        return app
