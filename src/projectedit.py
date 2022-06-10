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
@app.route('/new_project', methods = ['GET', 'POST'])
def new_project():
    """Handle new project form."""

    project_name = request.values.get('project_name')
    if not project_name:
        # Get worktypes and companies for selections
        query_worktypes = 'SELECT id, name, price FROM work_type'
        worktypes = db.session.execute(query_worktypes).fetchall()
        query_companies = 'SELECT id, name FROM company WHERE user_id = :uid'
        companies = db.session.execute(query_companies, {'uid': g.user})

        return render_template(
            'projectedit.html',
            worktypes = worktypes,
            companies = companies
        )

    worktype = request.values.get('worktype')
    if worktype:
        worktype = int(worktype)
    company = request.values.get('company')
    if company:
        company = int(company)

    # Create project according to action
    outcome = False
    action = request.values.get('action')
    if action == 'create':
        outcome = create_project(project_name, company, worktype)
    elif action == 'start':
        outcome = create_and_start_project(project_name, company, worktype)
    elif action == 'finish':
        outcome = create_and_finish_project(project_name, company, worktype)
    else:
        flash('Error with submit type. Please contact developers.')

    # Flash message when creation successful
    if outcome:
        flash('Project created successfully!')
    return redirect(url_for('manager'))


def validate_project(name: str, company: int):
    """Validate project name and company inputs."""

    # Validate project name
    name_regex = '^(?![ _.-])(?!.*[# _.-]{2})[\w# _.-]{4,128}(?<![# _.-])$'
    if re.match(name_regex, name) is None:
        flash('Invalid project name!')
        return False
    # Make sure a company is chosen
    if company < 1:
        flash('Select a company for project!')
        return  False
    return True


def create_project(name: str, company: int, worktype: int):
    """Create project and save it to db."""

    if not validate_project(name, company):
        return False
    
    insert = """INSERT INTO
                    project (name, state, user_id, company_id, type_id)
                VALUES
                    (:name, :state, :user_id, :company, :worktype)"""
    db.session.execute(
        insert,
        {
            'name': name,
            'user_id': g.user,
            'state': 1,         # 1 = active
            'company': company,
            'worktype': worktype
        }
    )
    db.session.commit()
    return True
    

def create_and_start_project():
    return


def create_and_finish_project():
    return