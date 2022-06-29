"""App homepage."""

from flask import render_template
from src import app
from src.login import require_login


@app.route('/user/<uid>')
@require_login()
def user(uid: int):
    """Render homepage."""

    return render_template('user.html')
