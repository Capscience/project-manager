from src.app import db

class Users(db.Model):
    """Login data for users."""

    uid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(32))
    password = db.Column(db.String(128))


class Companies(db.Model):
    """Companies that can be used as clients for projects."""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(32), unique = True)


class Entries(db.Model):
    """Project time entries."""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id',
                                                     ondelete = 'CASCADE'))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    comment = db.Column(db.String(128))


class Projects(db.Model):
    """Project data for users."""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    state = db.Column(db.Integer)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  ondelete = 'CASCADE'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id',
                                                     ondelete = 'CASCADE'))


db.create_all()
