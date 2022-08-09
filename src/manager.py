"""Module for handling main app view and data."""

from flask import render_template
from flask import g
from src import app
from src import db
from src.login import require_login


@app.route('/app')
@require_login()
def manager():
    """Handles the main app function."""

    # COALESCE("end", NOW()) makes running projects
    # show current time when page is refreshed
    query_active = """SELECT
                        P.id, P.name, C.name, P.state,
                        (SELECT
                            SUM(EXTRACT(EPOCH FROM
                            COALESCE("end", NOW()) - start))*interval '1 sec'
                            FROM entry WHERE project_id = P.id
                        ) as time,
                        (SELECT
                            comment
                        FROM
                            entry
                        WHERE
                            project_id = P.id
                            AND comment IS NOT NULL
                            AND comment != 'Rounding entry.'
                        LIMIT 1
                        ) as comment,
                        COALESCE(ROUND((SELECT
                            SUM(EXTRACT(EPOCH FROM
                            COALESCE("end", NOW()) - start))
                        FROM entry WHERE project_id = P.id
                        )::INTEGER * WT.price/3600
                        ,2),0) as price
                    FROM
                        project P, company C, work_type WT
                    WHERE
                        P.company_id = C.id
                        AND P.user_id = :uid
                        AND P.state > 0
                        AND P.type_id = WT.id
                    ORDER BY
                        P.state DESC, P.id DESC"""
    projects = db.session.execute(query_active, {'uid': g.user[0]}).fetchall()
    # Get projects stopped today
    query_stopped_today = """SELECT
                                P.id, P.name, C.name, P.state,
                                (SELECT
                                    SUM(EXTRACT(EPOCH FROM
                                    "end" - start))*interval '1 sec'
                                FROM entry WHERE project_id = P.id
                                ) as time,
                                (SELECT
                                    comment
                                FROM
                                    entry
                                WHERE
                                    project_id = P.id
                                    AND comment IS NOT NULL
                                    AND comment != 'Rounding entry.'
                                LIMIT 1
                                ) as comment,
                                ROUND((SELECT
                                    SUM(EXTRACT(EPOCH FROM
                                    "end" - start))
                                FROM entry WHERE project_id = P.id
                                )::INTEGER * WT.price/3600
                                ,2) as price
                            FROM
                                project P, company C, work_type WT
                            WHERE
                                P.company_id = C.id
                                AND P.user_id = :uid
                                AND P.state = 0
                                AND P.type_id = WT.id
                                AND (SELECT DATE(start)
                                     FROM entry
                                     WHERE project_id = P.id
                                     ORDER BY start ASC LIMIT 1
                                    ) = DATE(NOW())
                            ORDER BY
                                P.state DESC, P.id DESC"""
    stopped_today = db.session.execute(
        query_stopped_today,
        {
            'uid': g.user[0]
        }
    ).fetchall()
    # Get total work time for the day
    query_todays_time = """SELECT
                               SUM(EXTRACT(EPOCH FROM
                               COALESCE("end", NOW())-start))*interval '1 sec'
                           FROM
                               entry E, project P
                           WHERE
                               E.project_id = P.id
                               AND P.user_id = :uid
                               AND DATE(start) = DATE(NOW())"""
    todays_time = db.session.execute(
        query_todays_time,
        {'uid': g.user[0]}
    ).fetchone()

    return render_template(
        'manager.html',
        projects=projects,
        todays_time=todays_time[0],
        stopped_today=stopped_today
    )


@app.route('/app/finished')
@require_login()
def finished():
    """Show finished projects."""

    query_finished = """SELECT
                            P.id, P.name, C.name, P.state,
                            (SELECT
                                SUM(EXTRACT(EPOCH FROM
                                "end" - start))*interval '1 sec'
                                FROM entry WHERE project_id = P.id
                            ) as time,
                            (SELECT
                                comment
                            FROM
                                entry
                            WHERE
                                project_id = P.id
                                AND comment IS NOT NULL
                                AND comment != 'Rounding entry.'
                            LIMIT 1
                            ) as comment,
                            ROUND((SELECT
                                SUM(EXTRACT(EPOCH FROM
                                "end" - start))
                            FROM entry WHERE project_id = P.id
                            )::INTEGER * WT.price/3600
                            ,2) as price
                        FROM
                            project P, company C, work_type WT
                        WHERE
                            P.company_id = C.id
                            AND P.user_id = :uid
                            AND P.state = 0
                            AND P.type_id = WT.id
                        ORDER BY
                            P.company_id DESC, P.type_id DESC, P.id DESC"""
    projects = db.session.execute(
        query_finished,
        {
            'uid': g.user[0]
        }
    ).fetchall()
    return render_template(
        'finished.html',
        projects=projects,
    )
