import datetime
from flask import render_template
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import g
from src import app, db
from src.login import require_login


@app.route('/app')
@require_login()
def manager():
    """Handles the main app function."""

    # Get user's projects. E."end" is needed to determine whether project is running or paused
    query = """SELECT
                   P.id, P.name, C.name, P.state,
                   (SELECT SUM(EXTRACT(EPOCH FROM "end"-start))*interval '1 sec' as diff FROM entry WHERE project_id = P.id) as time
               FROM
                   project P, company C
               WHERE
                   P.company_id = C.id AND P.user_id=:uid
               ORDER BY
                   P.state DESC, P.id DESC"""
    projects = db.session.execute(query, {'uid': g.user}).fetchall()
    return render_template(
        'manager.html',
        projects = projects,
        timeformat = timeformat
    )


def timeformat(timedelta: datetime.timedelta) -> str:
    """Format timedelta object to HH:MM"""

    timedelta = timedelta.seconds
    hours = timedelta // 3600
    minutes = timedelta // 60 - (hours * 60)
    seconds = timedelta - (minutes*60) - (hours*3600)
    return f'{hours:02}:{minutes:02}:{seconds:02}'
