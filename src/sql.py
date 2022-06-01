from src import db

class Account(db.Model):
    """Login data for users."""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(32))
    password = db.Column(db.String(128))


class Company(db.Model):
    """Companies that can be used as clients for projects."""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(32), unique = True)


class Entry(db.Model):
    """Project time entries."""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id',
                                                     ondelete = 'CASCADE'))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    comment = db.Column(db.String(128))


class Project(db.Model):
    """Project data for users."""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    state = db.Column(db.Integer)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id',
                                                  ondelete = 'CASCADE'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id',
                                                     ondelete = 'CASCADE'))
    type_id = db.Column(db.Integer, db.ForeignKey('worktype.id'))


class WorkType(db.Model):
    """Templates for rounding and pricing different jobs."""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(32), unique = True)
    rounding = db.Column(db.Numeric)    # rounding parameter for hours
    minimum = db.Column(db.Numeric) # minumim hours
    price = db.Column(db.Numeric)   # price per hour

# Create all tables that don't exist yet
db.create_all()
