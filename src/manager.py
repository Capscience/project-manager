from flask import render_template
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import g
from src import app, db
from src.login import require_login


@app.route('/app')
@require_login()
def manager():
    """Handles the main app function."""

    # Get user's projects
    query = """SELECT P.id, P.name, C.name FROM project P, company C
               WHERE C.id=P.company_id AND P.user_id=:uid"""
    projects = db.session.execute(query, {'uid': g.user}).fetchall()
    return render_template(
        'manager.html',
        projects = projects,
    )
