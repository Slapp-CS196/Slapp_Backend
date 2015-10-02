from flask.ext.sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
 
class Slapp(Base):
    __tablename__ = 'slapps'
 
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
 
    def __init__(self, time, latitude, longitude):
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
 
    def __repr__(self):
        return '<Item %r>' % self.time