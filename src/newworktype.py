import re
import datetime
from flask import render_template
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from src import app, db
from src.login import require_login


@app.route('/new_worktype', methods = ['GET', 'POST'])
@require_login()
def new_worktype():
    """Create new worktypes."""

    if request.method == 'GET':
        return render_template('newworktype.html')

    # Get inputs from form
    name = request.values.get('name', '').strip()
    rounding = request.values.get('rounding', '').strip()
    rounding_unit = int(request.values.get('rounding_unit'))
    minimum = request.values.get('minimum', '').strip()
    min_unit = int(request.values.get('min_unit'))
    price = request.values.get('price', '0').strip()

    if create_worktype(
        name,
        rounding,
        rounding_unit,
        minimum,
        min_unit,
        price):
        flash('Worktype created successfully.')
        return redirect(url_for('manager'))
    return redirect(url_for('new_worktype'))


def create_worktype(
    name: str,
    rounding: str,
    rounding_unit: int,
    minimum: str,
    min_unit: int,
    price: str) -> bool:
    """Create worktype for all users to use."""

    # Validate worktype name
    name_regex = r'[\w _.-]{4,128}'
    if re.match(name_regex, name) is None:
        flash('Invalid name!')
        return False
    query_worktype = 'SELECT * FROM work_type WHERE name = :name'
    worktype = db.session.execute(query_worktype, {'name': name}).fetchone()
    if worktype is not None:
        flash('Worktype name is already taken.')
        return False

    # Validate numerical values
    try:
        minimum = int(minimum)
        rounding = int(rounding)
        price = int(price)
    except ValueError:
        flash('Only use integers for rounding, minimum and price!')
        return False
    
    # Set rounding and minimum to correct units
    if rounding_unit == 1:
        rounding = datetime.timedelta(minutes = rounding)
    elif rounding_unit == 2:
        rounding = datetime.timedelta(hours = rounding)
    
    if min_unit == 1:
        minimum = datetime.timedelta(minutes = minimum)
    elif min_unit == 2:
        minimum = datetime.timedelta(hours = minimum)

    # Create new worktype
    insert = """INSERT INTO work_type
                    (name, rounding, minimum, price)
                VALUES
                    (:name, :rounding, :minimum, :price)"""
    db.session.execute(
        insert,
        {
            'name': name,
            'rounding': rounding,
            'minimum': minimum,
            'price': price
        }
    )
    db.session.commit()
    return True
