from flask import render_template
from src import app


@app.route('/help')
def help():
    return render_template('help.html')
