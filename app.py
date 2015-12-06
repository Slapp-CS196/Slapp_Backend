import os
from flask import Flask, jsonify, request
from models import db, Slapp, User, Profile, Link
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

@app.route('/', methods=['GET'])
def test_working():
    return 'I think I\'m working kinda?'
@app.route('/api/newSlapp', methods=['GET'])
def newSlapp():
    if 'email' and 'time' and 'latitude' and 'longitude' and 'radius' in request.args:
        email = request.args['email']
        time = request.args['time']
        latitude = request.args['latitude']
        longitude = request.args['longitude']
        radius = request.args['radius']
        slapp = Slapp(email, time, latitude, longitude, radius)
        db.session.add(slapp)
        db.session.commit()
        return 'Slapp_added'
        '''slapps = Slapp.query.all()
        slapp_list = []
        for result in slapps:
            if abs(result.time - request.args['time']) < 1:
                if abs(result.latitude - request.args['latitude']) < request.args['radius'] + result.radius:
                    if abs(result.longitude - request.args['longitude']) < request.args['radius'] + result.radius:
                        new_slapp = {}
                        new_slapp['id'] = result.id
                        new_slapp['user_id'] = result.user_id
                        new_slapp['time'] = result.time
                        new_slapp['latitude'] = result.latitude
                        new_slapp['longitude'] = result.longitude
                        new_slapp['radius'] = result.radius
                        slapp_list.append(new_slapp)
        return jsonify(slapps=slapp_list)'''
    else:
        return 'Error, not enough parameters'
@app.route('/api/newUser', methods=['GET'])
def newUser():
    if 'email' and 'join_date' and 'username' and 'password' and 'first_name' and 'last_name' in request.args:
        user = User(request.args['email'],request.args['join_date'],request.args['username'],request.args['password'],request.args['first_name'],request.args['last_name'])
        db.session.add(user)
        db.session.commit()
        return 'User added'
    else:
        return 'Error, not enough parameters'
@app.route('/api/newProfile', methods=['GET'])
def newProfile():
    if 'email' and 'prof_name' in request.args:
        profile = Profile(request.args['email'],request.args['prof_name'])
        db.session.add(profile)
        db.session.commit()
        return 'Profile added'
    else:
        return 'Error, not enough parameters'
@app.route('/api/newLink', methods=['GET'])
def newLink():
    if 'email' and 'prof_id' and 'link_type' and 'link_data' in request.args:
        link = Link(request.args['link_type'],request.args['link_data'])
        db.session.add(link)
        db.session.commit()
        profile = db.session.query(Profile).filter(Profile.id==request.args['prof_id']).one()
        if profile.link_list != " ":
            profile.link_list = profile.link_list + "," + str(link.id)
        else:
            profile.link_list = link.id
        db.session.add(profile)
        db.session.commit()
        return 'Link added'
db.init_app(app)
if __name__ == '__main__':
    port = int(os.environ.get("PORT",80))
    app.run(host='0.0.0.0', port=port, debug=True)
