import re
from flask import render_template
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import g
from src import app, db
from src.login import require_login


@require_login()
@app.route('/new_company', methods = ['GET', 'POST'])
def new_company():
    """Handle new company form."""

    company_name = request.values.get('company_name')
    if company_name:
        if add_company(company_name):
            flash('Company added successfully!')
        return redirect(url_for('manager'))
    return render_template('companyedit.html')


def add_company(name: str):
    """Validate input and add valid company to db."""

    # Validate name
    name_regex = '^(?![ _.-])(?!.*[ _.-]{2})[\w _.-]{4,128}(?<![ _.-])$'
    if re.match(name_regex, name) is None:
        flash('Invalid company name!')
        return False
    # Check for same name company in db
    query = 'SELECT * FROM company WHERE name=:name AND user_id=:uid'
    company = db.session.execute(query, {'name': name, 'uid': g.user}).fetchone()
    if company is not None and company[1] == name:
        flash(f'There already exists a compnay with that name.')
        return False
    # If all checks successful, create company
    insert = 'INSERT INTO company (name, user_id) VALUES (:name, :uid)'
    db.session.execute(insert, {'name': name, 'uid': g.user})
    db.session.commit()
    return True
