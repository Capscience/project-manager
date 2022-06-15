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
@app.route('/delete/<pid>', methods = ['GET', 'POST'])
def delete(pid: int):
    """Handle deleting specified project."""

    print(request.method)

    query_project = 'SELECT * FROM project WHERE id=:pid AND user_id=:uid'
    project = db.session.execute(query_project, {'pid': pid, 'uid': g.user}).fetchone()
    if project is None:
        flash('Project not found, and therefore not deleted.')
        return redirect(url_for('manager'))
    if request.method == 'POST':
        delete = 'DELETE FROM project WHERE id=:pid'
        db.session.execute(delete, {'pid': pid})
        db.session.commit()
        flash('Project deleted.')
        return redirect(url_for('manager'))
    else:
        return render_template('delete.html', project = project)
