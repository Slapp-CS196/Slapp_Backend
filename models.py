from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Slapp(db.Model):
    __tablename__ = 'slapps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    time = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, time, latitude, longitude):
        self.time = time
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Item %r>' % self.time