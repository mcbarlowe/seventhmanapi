'''Creating Flask application factory'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# this has to go after the code above or else it cant import
# the db class to query the database
from seventhman.stats.controllers import stats
app.register_blueprint(stats)
