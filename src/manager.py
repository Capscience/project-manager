from flask import render_template
from flask import redirect
from flask import render_template
from flask import session
from flask import request
from flask import url_for
from flask import flash
from src import app, db
from src.login import require_login
from src import sql

@app.route('/app', methods = ['GET', 'POST'])
@require_login()
def manager():
    """Handles the main app function."""

    name = request.values.get('name')
    if name:
        if validate_company_name(name):
            db.session.add(sql.Company(name = name))
            db.session.commit()
    companies = sql.Company.query.all()
    return render_template('manager.html', companies = companies)

def validate_company_name(name: str):
    """Validate company name and add to database."""

    if len(name) < 4 or name.count(' ') > 1:
        flash('Company name should be at least 4 characters and contain no more than 1 space')
        return False
    db_name = sql.Company.query.filter_by(name = name).one_or_none()
    if db_name == name:
        flash(f'There already exists a compnay with name {name}.')
        return False
    return True
            