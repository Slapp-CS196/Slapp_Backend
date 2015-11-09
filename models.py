from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Slapp(db.Model):
    __tablename__ = 'slapps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius = db.Column(db.Integer)

    def __init__(self, user_id, time, latitude, longitude, radius):
        self.user_id = user_id
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius

    def __repr__(self):
        return '<Item %r>' % self.time
class User(db.Model):
     __tablename__ = 'users'

     id = db.Column(db.Integer, primary_key=True)
     email = db.Column(db.String)
     join_date = db.Column(db.Integer)
     username = db.Column(db.String(30))
     passwrod = db.Column(db.String(80))
     
     def __init__(self, email, join_date, username, password):
	self.email = email
	self.join_date = join_date
	self.username = username
	self.password = password
     def __repr__(self):
	return '<Item %r>' % self.username
