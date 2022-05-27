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
    pass
try:
    database_url = getenv("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(getenv('SECRET_KEY'))
    app.secret_key = getenv("SECRET_KEY")
except:
    print('Secret key or database url not found')

db = SQLAlchemy(app)
db.create_all()

# Import files including pages after app is created
import src.login
import src.user

@app.route('/')
def home():
    if g.user:
        return redirect(url_for('user', usr=g.user))
    return render_template('home.html')

@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == '__main__':
    app.run()