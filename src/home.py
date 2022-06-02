import imp
from flask import redirect
from flask import g
from flask import render_template
from flask import url_for
from src import app

@app.route('/')
def home():
    return render_template('home.html')
