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


@app.route('/new_company', methods = ['GET', 'POST'])
@require_login()
def new_company():
    """Handle new company form."""

    if request.method == 'GET':
        return render_template('newcompany.html')
    company_name = request.values.get('company_name', '').strip()
    if add_company(company_name):
        flash('Company added successfully!')
    return redirect(url_for('manager'))


def add_company(name: str):
    """Validate input and add valid company to db."""

    # Validate name
    name_regex = r'[\w _.-]{4,128}'
    if re.match(name_regex, name) is None:
        flash('Invalid company name!')
        return False
    # Check for same name company in db
    query = 'SELECT * FROM company WHERE name=:name AND user_id=:uid'
    company = db.session.execute(query, {'name': name, 'uid': g.user[0]}).fetchone()
    if company is not None and company[1] == name:
        flash(f'There already exists a company with that name.')
        return False
    # If all checks successful, create company
    insert = 'INSERT INTO company (name, user_id) VALUES (:name, :uid)'
    db.session.execute(insert, {'name': name, 'uid': g.user[0]})
    db.session.commit()
    return True
