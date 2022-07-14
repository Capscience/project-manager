"""List customers."""

from flask import render_template
from flask import g
from src import app
from src import db
from src.login import require_login


@app.route('/companylist')
@require_login()
def companylist() -> str:
    """Route for listing user's companies."""

    company_query = 'SELECT * FROM company WHERE user_id=:uid'
    companies = db.session.execute(company_query, {'uid': g.user[0]})
    return render_template('companylist.html', companies=companies)
