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
@app.route('/edit_project/<pid>', methods = ['GET', 'POST'])
def edit_project(pid: int):
    """Handle new project form."""

    if request.method == 'POST':
        get_edit_data(pid)
        return redirect(url_for('manager'))

    query_worktypes = 'SELECT id, name, price FROM work_type'
    worktypes = db.session.execute(query_worktypes).fetchall()
    query_companies = 'SELECT id, name FROM company WHERE user_id = :uid'
    companies = db.session.execute(query_companies, {'uid': g.user}).fetchall()
    query_project = """SELECT id, name, state, company_id, type_id
                       FROM project WHERE id = :pid AND user_id = :uid"""
    project = db.session.execute(query_project, {'pid': pid, 'uid': g.user}).fetchone()
    if project is None:
        flash('No project found.')
        return redirect(url_for('manager'))
    query_entries = """SELECT start, "end", "end"-start, comment
                       FROM entry WHERE project_id = :pid"""
    entries = db.session.execute(query_entries, {'pid': pid}).fetchall()

    return render_template(
        'projectedit.html',
        project = project,
        worktypes = worktypes,
        companies = companies,
        entries = entries
    )
    

def get_edit_data(pid: int):
    """Handle project edit form data."""

    # Get data from form
    project_name = request.values.get('project_name', '').strip()
    worktype = request.values.get('worktype')
    if worktype:
        worktype = int(worktype)
    company = request.values.get('company')
    if company:
        company = int(company)
    return