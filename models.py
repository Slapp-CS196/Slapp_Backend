from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Slapp(db.Model):
    __tablename__ = 'slapps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    time = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    readius = db.Column(db.Integer)

    def __init__(self, user_id, time, latitude, longitude, radius):
        self.user_id = user_id
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius

    def __repr__(self):
        return '<Item %r>' % self.time