"""Project manager"""

import importlib
import glob
import os
from flask import Flask
from flask import render_template
from flask import g
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Config file example in GitHub
try:
    app.config.from_pyfile('manager.conf')
except FileNotFoundError:
    # Secondary method is using environment variables
    database_url = os.getenv("DATABASE_URL").replace('postgres', 'postgresql+psycopg2')
    if database_url is None:
        raise EnvironmentError('Environment variable DATABASE_URL is not defined.')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    secret_key = os.getenv("SECRET_KEY")
    if secret_key is None:
        raise EnvironmentError('Environment variable SECRET_KEY is not defined.')
    app.secret_key = secret_key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import files including pages after app is created
for filename in sorted(glob.glob(os.path.dirname(__file__) + '/*.py')):
    module = os.path.basename(filename)[:-3]      # Without ".py"                                                                                                                           
    if module != '__init__':
        importlib.import_module('src.' + module)
