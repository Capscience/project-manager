"""App homepage."""

from flask import render_template
from flask import abort
from flask import g
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
from src import app
from src import db
from src.login import require_login


@app.route('/user/<uid>', methods=['GET', 'POST'])
@require_login()
def user(uid: str):
    """Render user page and handle user deletion."""

    if int(uid) != g.user[0]:
        abort(403)

    if request.values.get('action') == 'delete':
        delete_sql = 'DELETE FROM account WHERE id=:uid'
        db.session.execute(delete_sql, {'uid': g.user[0]})
        db.session.commit()
        flash('User deleted successfully.')
        return redirect(url_for('logout'))
    return render_template('user.html')
