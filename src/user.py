from flask import render_template
from flask import g
from flask import redirect
from flask import url_for
from src import app

@app.route('/user')
def user():
    if not g.user:
        return redirect(url_for('home'))
    return render_template('manager.html')