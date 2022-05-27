from flask import render_template
from flask import g
from flask import redirect
from flask import url_for
from src.app import app

@app.route('/<usr>')
def user(usr):
    if not g.user:
        return redirect(url_for('home'))
    return render_template('user.html')