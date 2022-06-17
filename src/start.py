from flask import redirect
from flask import g
from flask import url_for
from src import app, db
from src.login import require_login


@app.route('/start/<pid>')
@require_login()
def start(pid: int) -> str:
    """Create start entry for project with given pid."""

    if validate_start(pid):
        # Create entry
        insert = 'INSERT INTO entry (project_id, start) VALUES (:pid, NOW())'
        db.session.execute(insert, {'pid': pid})
        # Switch state to 'running'
        update = 'UPDATE project SET state=2 WHERE id=:pid'
        db.session.execute(update, {'pid': pid})
        db.session.commit()
    return redirect(url_for('manager'))

def validate_start(pid: int) -> bool:
    """Check if project with pid can be started."""

    # Validate pid
    query = 'SELECT state FROM project WHERE user_id=:uid AND id=:pid'
    project = db.session.execute(query, {'uid': g.user[0], 'pid': pid}).fetchone()
    # Make sure that project exists and isn't in 'stopped' state
    if project is None or project[0] == 0:
        return False
    
    # Check if project is running
    query = 'SELECT * FROM entry WHERE project_id=:pid ORDER BY id DESC'
    entry = db.session.execute(query, {'pid': pid}).fetchone()
    # example entry: (1, 1, datetime.datetime(2022, 6, 10, 21, 47, 34, 798696), None, None)
    if entry is None:
        return True
    if entry[3] is None and entry[2] is not None: # Has start but no end time -> running
        return False
    return True
