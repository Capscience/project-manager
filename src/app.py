"""Project manager"""

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Config file example in GitHub
app.config.from_pyfile('manager.conf')
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('home.html')
