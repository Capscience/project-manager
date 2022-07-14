"""Edit company."""

from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import g
from src import app
from src import db
from src.login import require_login


@app.route('/edit_company/<cid>', methods=['GET', 'POST'])
@require_login()
def edit_company(cid):
    """Route for editing companies."""

    # Validate project
    query = 'SELECT * FROM company WHERE id=:cid AND user_id=:uid'
    company = db.session.execute(query, {'cid': cid, 'uid': g.user[0]})
    if not company:
        return redirect(url_for('companylist'))
    if request.method == 'GET':
        return render_template('companyedit.html', company=company)
    action = request.values.get('action')
    if action == 'delete':
        delete(cid)
    elif action == 'save':
        if not validate_and_save(cid):
            return redirect(url_for('edit_company', cid=cid))
    return redirect(url_for('manager'))


def delete(cid):
    """Delete project."""

    delete_sql = 'DELETE FROM company WHERE id=:cid'
    db.session.execute(delete_sql, {'cid': cid})
    db.session.commit()
    flash('Customer deleted.')


def validate_and_save(cid):
    """Validate renaming and save."""

    name = request.values.get('name').strip()
    if not (name and 3 < len(name) < 128):
        flash('Name length invalid.')
        return False
    update = 'UPDATE company SET name=:name WHERE id=:cid'
    db.session.execute(update, {'name': name, 'cid': cid})
    db.session.commit()
    flash('Renaming successful.')
    return True
