from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Slapp(db.Model):
    __tablename__ = 'slapps'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40))
    time = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius = db.Column(db.Integer)
    matched_id = db.Column(db.Integer)

    def __init__(self, email, time, latitude, longitude, radius):
        self.email = email
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.matched_id = -1

    def __repr__(self):
        return '<Item %r>' % self.time
class User(db.Model):
     __tablename__ = 'users'

     id = db.Column(db.Integer, primary_key=True)
     email = db.Column(db.String(40))
     join_date = db.Column(db.String(50))
     password = db.Column(db.String(80))
     curr_profile = db.Column(db.Integer)
     first_name = db.Column(db.String(30))
     last_name = db.Column(db.String(30))
     
     def __init__(self, email, password, first_name, last_name):
    	self.email = email
    	self.join_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    	self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.curr_profile = -1
     def __repr__(self):
	   return '<Item %r>' % self.email
class Profile(db.Model):
     __tablename__ = 'profiles'

     id = db.Column(db.Integer, primary_key=True)
     email = db.Column(db.String(40))
     prof_name = db.Column(db.String(30))
     link_list = db.Column(db.String(80))

     def __init__(self, email, prof_name):
        self.email = email
        self.prof_name = prof_name
        self.link_list = " "
     def __repr__(self):
        return '<Item %r>' % self.prof_name
class Link(db.Model):
     __tablename__ = 'links'

     id = db.Column(db.Integer, primary_key=True)
     link_type = db.Column(db.String(50))
     link_data = db.Column(db.String(100))
 
     def __init__(self, link_type, link_data):
        self.link_type = link_type
        self.link_data = link_data
     def __repr__(self):
        return '<Item %r>' % self.link_type
