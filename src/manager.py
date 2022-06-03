from concurrent.futures.process import _threads_wakeups
from flask import render_template
from flask import redirect
from flask import render_template
from flask import session
from flask import request
from flask import url_for
from flask import flash
from flask import g
from src import app, db
from src.login import require_login
from src import sql


@app.route('/app', methods = ['GET', 'POST'])
@require_login()
def manager():
    """Handles the main app function."""

    # Create new company
    company_name = request.values.get('company_name')
    if company_name:
        if add_company(company_name):
            flash('Company added successfully!')
        return redirect(url_for('manager'))

    # Create new project
    project_name = request.values.get('project_name')
    worktype = request.values.get('worktype')
    if worktype:
        worktype = int(worktype)
    company = request.values.get('company')
    if company:
        company = int(company)
    if project_name:
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

    # Get needed data from database
    projects = sql.Project.query.filter_by(user_id = g.user)
    for project in projects:
        print(project.name)
    types = sql.WorkType.query.all()
    for worktype in types:
        print(worktype.name)
    companies = sql.Company.query.all()
    for company in companies:
        print(company.name)
    return render_template(
        'manager.html',
        companies = companies,
        projects = projects,
        worktypes = types,
        sql = sql
    )


def add_company(name: str):
    """Validate input and add valid company to db."""

    # Validate name
    if len(name) < 4 or len(name) > 128 or name.count(' ') > 2:
        flash('Company name should be 4-128 characters and contain no more than 2 spaces.')
        return False
    # Check for same name company in db
    company = sql.Company.query.filter_by(name = name, user_id = g.user).one_or_none()
    if  company is not None and company.name == name:
        flash(f'There already exists a compnay with that name.')
        return False
    # If all checks successful, create company
    db.session.add(sql.Company(name = name, user_id = g.user))
    db.session.commit()
    return True


def validate_project(name: str, company: int):
    """Validate project name and company inputs."""

    # Validate project name length
    if len(name) < 4 or len(name) > 128:
        flash('Please give the project a 4-128 character name.')
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
    
    db.session.add(sql.Project(
        name = name,
        state = 1,  # 1 = active
        user_id = g.user,
        company_id = company,
        type_id = worktype
    ))
    db.session.commit()
    return True
    

def create_and_start_project():
    return


def create_and_finish_project():
    return