import os
from flask import Flask, jsonify, request
from models import db, Slapp, User, Profile, Link
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
currentSlappId = 0

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
	id = currentSlappId
	currentId = currentSlappId + 1
        slapp = Slapp(id, email, time, latitude, longitude, radius)
        db.session.add(slapp)
        db.session.commit()
        return 'Slapp' + str(slapp.id) + 'added'
    else:
        return 'Error, not enough parameters'
@app.route('/api/newUser', methods=['GET'])
def newUser():
    if 'email' and 'password' and 'first_name' and 'last_name' in request.args:
        user = User(request.args['email'],request.args['password'],request.args['first_name'],request.args['last_name'])
        db.session.add(user)
        db.session.commit()
        return 'User ' + str(user.email) + ' added'
    else:
        return 'Error, not enough parameters'
@app.route('/api/newProfile', methods=['GET'])
def newProfile():
    if 'email' and 'prof_name' in request.args:
        profile = Profile(request.args['email'],request.args['prof_name'])
        db.session.add(profile)
        db.session.commit()
        return str(profile.id)
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
        return 'Link ' + str(link.id) + ' added'
    else:
        return 'Error, not enough parameters'
@app.route('/api/setActiveProf', methods=['GET'])
def setActive():
    if 'email' and 'prof_id' in request.args:
        user = db.session.query(User).filter(User.email==request.args['email']).first()
        user.curr_profile = request.args['prof_id']
        db.session.add(user)
        db.session.commit()
        return 'Active Profile Updated'
    else:
        return 'Error, not enough parameters'
@app.route('/api/getActiveProf', methods=['GET'])
def getActiveProf():
    if 'email' in request.args:
        user = db.session.query(User).filter(User.email==request.args['email']).first()
        return str(user.curr_profile)
    else:
        return 'Error, not enough parameters'
@app.route('/api/getUserProfs', methods=['GET'])
def getProfiles():
    if 'email' in request.args:
        profiles = db.session.query(Profile).filter(Profile.email==request.args['email'])
        profString = ""
        for profile in profiles:
            if profString == "":
                profString = str(profile.id)
            else:
                profString = profString + "," + str(profile.id)
        return profString
    else:
        return 'Error, not enough parameters'
@app.route('/api/getProfName', methods=['GET'])
def getProfName():
    if 'prof_id' in request.args:
        profile = db.session.query(Profile).filter(Profile.id==request.args['prof_id']).first()
        if profile is None:
            return 'Profile not found'
        else:
            return profile.prof_name
    else:
        return 'Error, not enough parameters'
@app.route('/api/getProfData', methods=['GET'])
def getProfData():
    if 'prof_id' in request.args:
        profile = db.session.query(Profile).filter(Profile.id==request.args['prof_id']).one()
        link_ids = profile.link_list.split(",")
        links = db.engine.execute("SELECT * FROM links WHERE id IN (" + profile.link_list + ")")
        dataList = ""
        for link in links:
            if dataList == "":
                dataList = link.link_type + ":" + link.link_data
            else:
                dataList = dataList + "," + link.link_type + ":" + link.link_data
        return 'test' + dataList
    else:
        return 'Error, not enough parameters'
@app.route('/api/getMatch', methods=['GET'])
def getMatch():
    if 'id' in request.args:
        slapp = db.session.query(Slapp).filter(Slapp.id==request.args['id']).one()
        matchList = db.engine.execute("SELECT * FROM slapps WHERE id != " + request.args['id'] + " AND abs(longitude - " + str(slapp.longitude) + ") < (radius + " + str(slapp.radius) + ") AND ABS(time - " + str(slapp.time) + ") < 2000 AND ABS(latitude - " + str(slapp.latitude) + ") < (radius + " + str(slapp.radius) + ")")
        bestScore = 999999
        match_id = -1
        for match in matchList:
            matchScore = abs(match.longitude - slapp.longitude)**2 + abs(match.latitude - slapp.latitude)**2 + abs(match.time - slapp.time)
            if matchScore < bestScore:
                match_id = match.id
                bestScore = matchScore
        if match_id != -1:
            matchSlapp = db.engine.execute("SELECT * FROM slapps WHERE id = " + str(match_id))
            for slapp in matchSlapp:
                return slapp.email
        else:
            return 'No Match'
    else:
        return 'Error, not enough parameters'
@app.route('/api/getLogin', methods=['GET'])
def getLogin():
    if 'email' and 'password' in request.args:
        accounts = db.engine.execute("SELECT * FROM users WHERE email = '" + request.args['email'] + "'")
        for account in accounts:
            if account.password == request.args['password']:
                return 'Login success'
        return 'Invalid login'
    else:
        return 'Error, not enough parameters'
@app.route('/api/getActiveProfName', methods=['GET'])
def getActiveProfName():
    if 'email' in request.args:
       user = db.session.query(User).filter(User.email==request.args['email']).first()
       curr_profile = user.curr_profile
       if curr_profile == -1:
           return str(curr_profile)
       else:
           profile = db.session.query(Profile).filter(Profile.id==curr_profile).first()
           return str(profile.prof_name)
    else:
       return 'Error, not enough parameters'
@app.route('/api/removeProf', methods=['GET'])
def delProf():
    if 'prof_id' in request.args:
        db.session.query(Profile).filter(Profile.id==request.args['prof_id']).delete()
        db.session.commit()
        return 'Profile deleted'
    else:
        return 'Error, not enough parameters'
db.init_app(app)
if __name__ == '__main__':
    port = int(os.environ.get("PORT",80))
    app.run(host='0.0.0.0', port=port, debug=True)
