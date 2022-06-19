"""App homepage."""

from flask import render_template
from src import app


@app.route('/')
def home():
    """Render homepage."""

    return render_template('home.html')
