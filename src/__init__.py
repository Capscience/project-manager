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
    try:
        database_url = os.getenv("DATABASE_URL").replace('postgres', 'postgresql+psycopg2')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(os.getenv('SECRET_KEY'))
        app.secret_key = os.getenv("SECRET_KEY")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    except:
        print('Secret key or database url not found')

db = SQLAlchemy(app)

# Import files including pages after app is created
for filename in sorted(glob.glob(os.path.dirname(__file__) + '/*.py')):
    module = os.path.basename(filename)[:-3]      # Without ".py"                                                                                                                           
    if module != '__init__':
        importlib.import_module('src.' + module)
