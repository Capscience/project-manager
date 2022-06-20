"""Handles creating a new project."""

import re
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import g
from src import app, db
from src.login import require_login


@app.route('/new_project', methods=['GET', 'POST'])
@require_login()
def new_project():
    """Handle new project form."""

    if request.method == 'POST':
        next_page = create_project()
        return redirect(next_page)

    # Get worktypes and companies for selections
    query_worktypes = 'SELECT id, name, price FROM work_type'
    worktypes = db.session.execute(query_worktypes).fetchall()
    query_companies = 'SELECT id, name FROM company WHERE user_id = :uid'
    companies = db.session.execute(
        query_companies,
        {
            'uid': g.user[0]
        }
    ).fetchall()
    if companies == []:
        flash('You need to create a company before you can create a project.')

    return render_template(
        'newproject.html',
        worktypes=worktypes,
        companies=companies
    )


def validate_project(name: str, company: int):
    """Validate project name and company inputs.

    Args:
        name: Name given for project.
        company: Selected company id for whick the project is assigned.

    Returns:
        True if name is valid and company created.
        False othervise."""

    # Validate project name
    name_regex = r'^[\w _.#-]{4,128}$'
    if re.match(name_regex, name) is None:
        flash('Invalid project name!')
        return False
    # Make sure a company is chosen
    if company < 1:
        flash('Select a company for project!')
        return False
    return True


def create_project() -> str:
    """Create project and save it to database.

    Args:
        name: Name given for new project.
        company: Company id for which the project is assigned.
        worktype: Project's worktype id.
        action: Determines if project will be started or finished at creation.

    Returns:
        URL for next page.
    """

    # Get form data
    name = request.values.get('project_name', '').strip()
    worktype = request.values.get('worktype')
    if worktype:
        worktype = int(worktype)
    company = request.values.get('company')
    if company:
        company = int(company)

    # Create project according to action
    action = request.values.get('action')
    if action not in ('create', 'start', 'finish'):
        flash('Error with submit type. Please contact developers.')
        return url_for('manager')

    # Creation failed
    if not validate_project(name, company):
        return url_for('new_project')

    insert = """INSERT INTO
                    project (name, state, user_id, company_id, type_id)
                VALUES
                    (:name, :state, :user_id, :company, :worktype)
                RETURNING id"""
    pid = db.session.execute(
        insert,
        {
            'name': name,
            'user_id': g.user[0],
            'state': 1,         # 1 = active
            'company': company,
            'worktype': worktype
        }
    ).fetchone()
    db.session.commit()

    # Creation succesful, execute different actions
    if action == 'start':
        return url_for('start', pid=pid[0])
    if action == 'finish':
        return url_for('stop', pid=pid[0])
    return url_for('manager')
