"""Handles login and logout."""

import re
import functools
from flask import g
from flask import redirect
from flask import render_template
from flask import session
from flask import request
from flask import url_for
from flask import flash
from flask import abort
from passlib.hash import sha512_crypt
from src import app, db


def require_login():
    """Make sure there is a user logged in.

    DECORATOR MUST BE PLACED BETWEEN @app.route(...) and
    def func(): row TO WORK!
    """

    def decorator(func):
        """Check access decorator."""

        @functools.wraps(func)
        def decorated_function(*args, **kwargs):
            """Check that user is logged in."""

            if g.user is None:
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator


def hash_passwd(password) -> str:
    """Return password hash as string."""

    return sha512_crypt.hash(password)


def validate_passwd(user, password, user_password) -> bool:
    """Validate user's password."""

    return user and password and sha512_crypt.verify(password, user_password)


@app.before_first_request
@app.before_request
def before_request():
    """Entry function to define g.user."""

    g.user = session.get('user')


@app.route('/', methods=['GET', 'POST'])
def login():
    """Log in to the app."""

    if g.user:
        return redirect(url_for('manager'))

    if request.method == 'GET':
        return render_template('login.html')

    # Create new login
    invalidate_login()
    name = request.values.get('username', '').strip()
    password = request.values.get('password', '').strip()

    query = 'SELECT id, name, password FROM account WHERE name=:name'
    result = db.session.execute(query, {'name': name}).fetchone()
    # If user doesn't exist, redirect to register page
    if not result:
        flash('Invalid username or password.')
        return redirect(url_for('login'))
    # If login succesful, set session user
    if validate_passwd(result[1], password, result[2]):
        session['user'] = (result[0], result[1])
        return redirect(url_for('manager'))
    # Flash error message if login unsuccessful
    flash('Invalid username or password.')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""

    if g.user:
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('register.html')

    # Create new user
    invalidate_login()
    name = request.values.get('username', '').strip()
    password = request.values.get('password', '').strip()
    repeat_pw = request.values.get('repeat_pw', '').strip()

    invalid_name = False
    invalid_pw = False
    invalid_repeat_pw = False
    username_taken = False

    name_regex = r'^[\w_.-@]{3,128}$'
    if re.match(name_regex, name) is None:
        flash('Invalid username. Please refer to instructions for username.')
        invalid_name = True
    if len(password) < 10:
        flash('Password must be at least 10 characters.')
        invalid_pw = True
    if password != repeat_pw:
        flash('Please enter matching passwords!')
        invalid_repeat_pw = True
    # Username taken?
    query = 'SELECT id, name, password FROM account WHERE name=:name'
    result = db.session.execute(query, {'name': name}).fetchone()
    if result:
        flash('Username already exists.')
        username_taken = True

    if invalid_name or invalid_pw or invalid_repeat_pw or username_taken:
        return redirect(url_for('register'))

    # Successful creation of new user
    password = hash_passwd(password)
    insert = 'INSERT INTO account (name, password) VALUES (:name, :password)'
    db.session.execute(insert, {'name': name, 'password': password})
    db.session.commit()
    flash(f'User {name} has been successfully created.')
    return redirect(url_for('login'))


def invalidate_login():
    """Remove all current user information from session."""

    session.pop('user', None)
    g.user = None


@app.route('/logout')
def logout():
    """Log out from the app."""

    invalidate_login()
    return redirect(url_for('login'))
