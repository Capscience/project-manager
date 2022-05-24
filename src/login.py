"""Handles login and logout."""

import functools
from flask import g
from flask import redirect
from flask import render_template
from flask import session
from flask import request
from flask import url_for
from flask import flash
from passlib.hash import sha512_crypt
from app import app
import sql

def require_login():
    """Check that user is logged in when accessing app."""

    def decorator(func):
        """Check access decorator."""

        @functools.wraps(func)
        def decorated_function(*args, **kwargs):
            """Check that user is logged in."""

            if not g.user:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return decorated_function
    return decorator

def hash_passwd(password) -> str:
    """Return password hash as string."""

    return sha512_crypt.hash(password)

def validate_passwd(user, password) -> bool:
    """Validate user's password."""

    return user and password and sha512_crypt.verify(password, user.password)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Log in to the app."""

    if g.user:
        return redirect(url_for('/'))
    
    # Create new login
    invalidate_login()
    name = request.values.get('username')
    password = request.values.get('password')
    if name and password:
        user = sql.Users.query.filter_by(name = name).one_or_none()
        if validate_passwd(user, password):
            session['user'] = user.name
            return redirect(url_for('home'))
        flash('Invalid username or password.')

    return render_template('login.html')

def invalidate_login():
    """Remove all current user information from session."""

    session.pop('user', None)
    g.user = None

@app.route('/logout')
def logout():
    """Log out from the app."""

    invalidate_login()
    return url_for('home')