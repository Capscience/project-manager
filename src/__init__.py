"""Project manager"""

from os import getenv
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
        database_url = getenv("DATABASE_URL").replace('postgres', 'postgresql+psycopg2')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(getenv('SECRET_KEY'))
        app.secret_key = getenv("SECRET_KEY")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    except:
        print('Secret key or database url not found')

db = SQLAlchemy(app)

# Import files including pages after app is created
from src import login
from src import user

@app.route('/')
def home():
    if g.user:
        return redirect(url_for('user', usr=g.user))
    return render_template('home.html')

@app.route('/help')
def help():
    return render_template('help.html')
