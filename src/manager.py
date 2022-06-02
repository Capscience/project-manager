from flask import render_template
from src import app
from src.login import require_login

@app.route('/app')
@require_login()
def manager():
    return render_template('manager.html')
