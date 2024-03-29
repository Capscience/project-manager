"""Module that handles editing entries."""

from datetime import datetime
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask import g
from src import app
from src import db
from src.login import require_login


@app.route('/edit_entry/<eid>', methods=['GET', 'POST'])
@require_login()
def edit_entry(eid: int):
    """Handle new project form."""

    query_entry = """SELECT
                         id, start, "end", "end"-start, comment, project_id
                     FROM entry WHERE id = :eid"""
    entry = db.session.execute(query_entry, {'eid': eid}).fetchone()

    if entry is None:
        flash('Entry not found.')
        return redirect(url_for('manager'))

    # Project must be checked to make sure
    # entries can't be edited by other users.
    query_project = """SELECT id, state FROM project
                       WHERE id = :pid AND user_id = :uid"""
    project = db.session.execute(
        query_project,
        {
            'pid': entry[5],
            'uid': g.user[0]
        }
    ).fetchone()

    if project is None:
        flash('Entry not found.')
        return redirect(url_for('manager'))

    if request.method == 'POST':
        if request.values.get('action') == 'delete':
            delete(entry)
            return redirect(url_for('edit_project', pid=entry[5]))

        if validate_and_save(entry):
            flash('Editing successful.')
            if project[0] < 0:
                return redirect(url_for('manager'))
            else:
                return redirect(url_for('finished'))
        return redirect(url_for('edit_entry', eid=eid))

    return render_template('entryedit.html', entry=entry)


def validate_and_save(entry: tuple) -> bool:
    """Handle project edit form data.

    Args:
        entry: (id, start, "end", "end"-start, comment)
    """

    # Get data from form
    comment = request.values.get('comment', '').strip()
    start = request.values.get('start', '').strip()
    end = request.values.get('end', '').strip()

    # Check comment
    if comment:
        if 4 > len(comment) > 256:
            flash('Invalid comment!')
            return False
        edit_comment(comment, entry)

    # Make sure NULL times are not given a time
    # This could pause project without updating state
    if start and entry[1] is None:
        flash('You can not edit empty times!')
        return False
    if end and entry[2] is None:
        flash('You can not edit empty times!')
        return False

    update = update_entry(start, end, entry)
    if update:
        return True
    return False


def update_entry(start: str, end: str, entry: tuple):
    """Check edited values, and update if changed."""

    # Check for changes in values, and only update if something changed
    values = {}
    updates = []

    if start:
        try:
            start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            flash('Invalid time format!')
            return False
        values['start'] = start
        updates.append('start = :start')
    else:
        values['start'] = entry[1]

    if end:
        try:
            end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            flash('Invalid time format!')
            return False
        values['end'] = end
        updates.append('"end" = :end')
    else:
        values['end'] = entry[2] if entry[2] else datetime.now()

    if values['start'] > values['end']:
        flash('You can not make entry have negative time!')
        return False

    if len(updates) > 0:
        values['eid'] = entry[0]
        update = f"""UPDATE entry SET {', '.join(updates)}
                     WHERE id = :eid"""
        db.session.execute(update, values)
        db.session.commit()
    return True


def edit_comment(comment: str, entry: tuple) -> None:
    """Add comment that is already validated."""

    # Get latest entry
    query_entry = """SELECT comment
                     FROM entry
                     WHERE id = :eid"""
    old_comment = db.session.execute(query_entry, {'eid': entry[0]}).fetchone()

    if old_comment not in ['Rounding entry.', comment]:
        update = """UPDATE entry SET comment = :comment
                    WHERE id = :id"""
        db.session.execute(update, {'comment': comment, 'id': entry[0]})
        db.session.commit()
        return True
    return False


def delete(entry: tuple) -> None:
    """Delete entry with given id."""

    message = 'Entry deleted.'
    # Check if entry is rounding entry
    if entry[4] == 'Rounding entry.':
        # Reactivate project, else there can be finished projects
        # without rounding entry
        update = 'UPDATE project SET state=1 WHERE id=:pid'
        db.session.execute(update, {'pid': entry[5]})
        db.session.commit()
        message = 'Rounding entry deleted, and project reactivated.'

    if entry[1] and not entry[2]:
        # If entry to delete is running, set state to active
        update = 'UPDATE project SET state=1 WHERE id=:pid'
        db.session.execute(update, {'pid': entry[5]})
        db.session.commit()
        message = 'Running entry deleted, project paused.'

    delete_sql = 'DELETE FROM entry WHERE id=:eid'
    db.session.execute(delete_sql, {'eid': entry[0]})
    db.session.commit()
    flash(message)
