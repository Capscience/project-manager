"""Handle editing projects."""

import re
import datetime
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask import g
from src import app, db
from src.login import require_login


@app.route('/edit_project/<pid>', methods=['GET', 'POST'])
@require_login()
def edit_project(pid: int):
    """Handle project editing form."""

    query_project = """SELECT
                           P.id,
                           P.name,
                           P.state,
                           P.company_id,
                           P.type_id,
                           W.rounding
                       FROM
                           project P, work_type W
                       WHERE
                           P.id = :pid
                           AND P.user_id = :uid
                           AND P.type_id = W.id"""
    project = db.session.execute(
        query_project,
        {
            'pid': pid,
            'uid': g.user[0]
        }
    ).fetchone()

    if project is None:
        flash('No project found.')
        return redirect(url_for('manager'))

    if request.method == 'POST':
        if request.values.get('action') == 'save':
            if validate_and_save(project):
                flash('Editing successful.')
                return redirect(url_for('manager'))
            return redirect(url_for('edit_project', pid=pid))
        next_url = handle_actions(pid, project[5])
        return redirect(next_url)

    query_entries = """SELECT start, "end", "end"-start, comment, id
                       FROM entry WHERE project_id = :pid
                       ORDER BY id DESC"""
    entries = db.session.execute(
        query_entries,
        {
            'pid': pid
        }
    ).fetchall()

    query_worktypes = 'SELECT id, name, price FROM work_type'
    worktypes = db.session.execute(query_worktypes).fetchall()
    query_companies = """SELECT id, name FROM company
                         WHERE user_id = :uid"""
    companies = db.session.execute(
        query_companies,
        {
            'uid': g.user[0]
        }
    ).fetchall()

    return render_template(
        'projectedit.html',
        project=project,
        worktypes=worktypes,
        companies=companies,
        entries=entries
    )


def handle_actions(pid: int, rounding: datetime.timedelta) -> str:
    """Handle posts with action specified."""

    if request.values.get('action') == 'plus':
        add_rounding(pid, rounding)
        return url_for('edit_project', pid=pid)
    if request.values.get('action') == 'minus':
        remove_rounding(pid, rounding)
        return url_for('edit_project', pid=pid)
    if request.values.get('action') == 'delete':
        delete(pid)
        return url_for('manager')
    flash('Invalid action! Please contact developer!')
    return url_for('manager')


def validate_and_save(project: tuple) -> bool:
    """Handle project edit form data.

    Args:
        project: (id, name, state, company_id, type_id)
    """

    # Get data from form
    project_name = request.values.get('project_name', '').strip()
    comment = request.values.get('comment', '').strip()
    worktype = request.values.get('worktype')
    company = request.values.get('company')

    if comment:
        comment_regex = r'^[\w _.:#-]{4,256}$'
        if re.match(comment_regex, comment) is None:
            flash('Invalid comment!')
            return False
        add_comment(comment, project)

    update = update_project(project_name, worktype, company, project)
    if update:
        return True
    return False


def update_project(name: str, worktype: str, company: str, project: tuple):
    """Check edited values, and update if changed."""

    # Check for changes in values, and only update if something changed
    values = {}
    updates = []
    if name and name != project[1]:
        name_regex = r'^[\w _.,#-]{4,128}$'
        if re.match(name_regex, name) is None:
            flash('Invalid project name!')
            return False
        values['name'] = name
        updates.append('name = :name')

    if worktype:
        worktype = int(worktype)
        if worktype != project[4]:
            values['worktype'] = worktype
            updates.append('type_id = :worktype')
    if company:
        company = int(company)
        if company != project[3]:
            values['company'] = company
            updates.append('company_id = :company')

    if len(updates) > 0:
        values['pid'] = project[0]
        update = f"""UPDATE project SET {', '.join(updates)}
                     WHERE id = :pid"""
        db.session.execute(update, values)
        db.session.commit()
    return True


def add_comment(comment: str, project: tuple) -> None:
    """Add comment that is already validated."""

    # Get latest entry
    query_entry = """SELECT id, comment
                        FROM entry
                        WHERE project_id = :pid
                        ORDER BY id DESC"""
    entry = db.session.execute(query_entry, {'pid': project[0]}).fetchone()

    # If there are no entries, or latest entry has a comment,
    # create a comment only entry.
    if not entry or entry[1] is not None:
        # Times are not needed when entry order is by id
        insert = """INSERT INTO entry (project_id, comment)
                    VALUES (:pid, :comment)"""
        db.session.execute(insert, {'pid': project[0], 'comment': comment})
        db.session.commit()
    # If latest entry doesn't have a comment, update the comment there
    else:
        update = """UPDATE entry SET comment = :comment
                    WHERE id = :id"""
        db.session.execute(update, {'comment': comment, 'id': entry[0]})
        db.session.commit()


def delete(pid: int) -> None:
    """Delete project with given id."""

    delete_sql = 'DELETE FROM project WHERE id=:pid'
    db.session.execute(delete_sql, {'pid': pid})
    db.session.commit()
    flash('Project deleted.')


def add_rounding(pid: int, rounding: datetime.timedelta) -> None:
    """Add entry with time rounding."""

    insert = """INSERT INTO entry
                    (project_id, start, "end")
                VALUES
                    (:pid, NOW() - :rounding, NOW())"""
    db.session.execute(insert, {'pid': pid, 'rounding': rounding})
    db.session.commit()


def remove_rounding(pid: int, rounding: datetime.timedelta) -> None:
    """Add entry with time negative rounding."""

    insert = """INSERT INTO entry
                    (project_id, start, "end")
                VALUES
                    (:pid, NOW() + :rounding, NOW())"""
    db.session.execute(insert, {'pid': pid, 'rounding': rounding})
    db.session.commit()
