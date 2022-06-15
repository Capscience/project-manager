from flask import redirect
from flask import g
from flask import url_for
from src import app, db
from src.login import require_login


@require_login()
@app.route('/reactivate/<pid>')
def reactivate(pid: int) -> str:
    """Create start entry for project with given pid."""

    if validate_reactivation(pid):
        # Set state to 'active'
        update = 'UPDATE project SET state=1 WHERE id=:pid'
        db.session.execute(update, {'pid': pid})
        db.session.commit()
    return redirect(url_for('manager'))

def validate_reactivation(pid: int) -> bool:
    """Check if project with pid can be started."""

    # Validate pid
    query = 'SELECT state FROM project WHERE user_id=:uid AND id=:pid'
    project = db.session.execute(query, {'uid': g.user, 'pid': pid}).fetchone()
    # Make sure that project exists and isn't in 'stopped' state
    if project is None:
        return False
    if project[0] == 0:
        return True
    return False
