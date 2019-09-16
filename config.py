# enables dev env
DEBUG = True

#define application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#data base connection
SQLALCHEMY_DATABASE_URI = os.environ['NBA_CONNECT_DEV']
SQLALCHEMY_TRACK_MODIFICATIONS = True

#Application threads
THREADS_PER_PAGE = 2

# Enable protection against Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True


# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
