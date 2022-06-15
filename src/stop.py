"""Project stop button and time rounding."""

import datetime
from flask import redirect
from flask import g
from flask import render_template
from flask import url_for
from src import app, db
from src.login import require_login


@require_login()
@app.route('/stop/<pid>')
def stop(pid: int) -> str:
    """Finish project with pid."""

    if not validate_stop(pid):
        return redirect(url_for('manager'))
    rounded = add_rounding_entry(pid)


    return redirect(url_for('manager'))


def validate_stop(pid: int):
    """Check if project can be stopped."""

    # Validate pid
    query = 'SELECT state FROM project WHERE user_id=:uid AND id=:pid'
    project = db.session.execute(query, {'uid': g.user, 'pid': pid}).fetchone()
    if not project or project[0] == 0:
        return False
    
    # Check if project is running, pause if running
    query = 'SELECT * FROM entry WHERE project_id=:pid ORDER BY start DESC'
    entry = db.session.execute(query, {'pid': pid}).fetchone()
    # example entry: (1, 1, datetime.datetime(2022, 6, 10, 21, 47, 34, 798696), None, None)
    if entry is None:
        return True
    if entry[3] is None:    # No end time, so project is running
        # Set end value for entry
        update = 'UPDATE entry set "end"=NOW() WHERE project_id=:pid AND "end" IS NULL'
        db.session.execute(update, {'pid': pid})
        # Set state from 'running' to 'active' to show it's paused
        # 'Finished' state will be set when rounding 
        update = 'UPDATE project SET state=1 WHERE id=:pid'
        db.session.execute(update, {'pid': pid})
        db.session.commit()
    return True


def add_rounding_entry(pid: int) -> None:
    """Calculate needed timedelta, and save a rounding entry."""

    # Get total time of project
    query = """SELECT SUM(EXTRACT(EPOCH FROM ("end"-start)))*interval '1 sec' as diff
               FROM entry WHERE project_id = :pid"""
    tot_time = db.session.execute(query, {'pid': pid}).fetchone()
    tot_time = tot_time[0]  # Exctract timedelta object from tuple
    if tot_time is None:
        tot_time = datetime.timedelta(seconds = 0)

    # Get worktype data
    query = """SELECT W.name, W.rounding, W.minimum, W.price
               FROM work_type W, project P WHERE W.id=P.type_id AND P.id = :pid"""
    worktype = db.session.execute(query, {'pid': pid}).fetchone()
    rounding = worktype[1]  # rounding and minimum are datetime.timedelta objects
    minimum = worktype[2]

    # Check for minimum time
    if tot_time < minimum:
        rounded = minimum
    else:
        # TODO: rounding using timedeltas
        rounded = rounding * (tot_time // rounding + 1)
    delta = rounded - tot_time

    # Create rounding entry to database
    insert = """INSERT
                    INTO entry (project_id, start, "end", comment)
                VALUES
                    (:pid, NOW(), NOW() + :delta, 'Rounding entry.')"""
    db.session.execute(insert, {'pid': pid, 'delta': delta})
    # Update state to 'finished' or 'stopped'
    update = 'UPDATE project SET state=0 WHERE id=:pid'
    db.session.execute(update, {'pid': pid})
    db.session.commit()
    return
