"""App help page."""

from flask import render_template
from src import app


@app.route('/help')
def help_page():
    """Render help page."""

    return render_template('help.html')
