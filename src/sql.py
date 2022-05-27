from src.app import db

class Users(db.Model):
    """Login data for users."""

    name = db.Column(db.String(32), primary_key = True)
    password = db.Column(db.String(128))

db.create_all()
