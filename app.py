import os
from flask import Flask, jsonify, request
from models import db, Slapp
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

@app.route('/', methods=['GET'])
def test_working():
    return 'I think I\'m working kinda?'
@app.route('/api/new', methods=['GET'])
def create_new():
    if 'user_id' and 'time' and 'latitude' and 'longitude' and 'radius' in request.args:
        user_id = request.args['user_id']
        time = request.args['time']
        latitude = request.args['latitude']
        longitude = request.args['longitude']
        radius = request.args['radius']
        slapp = Slapp(user_id, time, latitude, longitude, radius)
        db.session.add(slapp)
        db.session.commit()
        slapps = Slapp.query.all()
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
        return jsonify(slapps=slapp_list)
    else:
        return 'Error, not enough parameters'

@app.route('/api/slapps', methods=['GET'])
def return_all():
    slapps = Slapp.query.all()
    slapp_list = []
    for result in slapps:
        new_slapp = {}
        new_slapp['id'] = result.id
        new_slapp['user_id'] = result.user_id
        new_slapp['time'] = result.time
        new_slapp['latitude'] = result.latitude
        new_slapp['longitude'] = result.longitude
        new_slapp['radius'] = result.radius
        slapp_list.append(new_slapp)
    return jsonify(slapps=slapp_list)
@app.route('/api/checkMatch' methods=['GET'])
def return_match():
    if 'latitude' and 'longitude' and 'radius' and 'curr_id' in request.args:
        my_slapp = db.engine.execute("SELECT * FROM slapps WHERE id = " + request.args['curr_id'])
        close_slapps = db.engine.execute("SELECT * FROM slapps WHERE ABS(latitude - " + request.args['latitude'] + ") < " + request.args['radius'] + " AND ABS(longitude - " + request.args['longitude'] + ") < " + request.args['radius'] + "AND id != " + request.args['curr_id'])
        best_match_id = -1
        best_match_score = 99999999
        #for possible_match in close_slapps:
        #    curr_match_score = 
    else:
        return "Not enough params"
@app.route('/api/nearby', methods=['GET'])
def return_nearby():
    if 'latitude' and 'longitude' and 'radius' in request.args:
        slapps = db.engine.execute("SELECT * FROM slapps WHERE ABS(latitude - " + request.args['latitude'] + ") < " + request.args['radius'] + " AND ABS(longitude - " + request.args['longitude'] + ") < " + request.args['radius'])
        slapp_list = []
        for result in slapps:
            new_slapp = {}
            new_slapp['id'] = result.id
            new_slapp['user_id'] = result.user_id
            new_slapp['time'] = result.time
            new_slapp['latitude'] = result.latitude
            new_slapp['longitude'] = result.longitude
            new_slapp['radius'] = result.radius
            slapp_list.append(new_slapp)
        return jsonify(nearby=slapp_list)
    else:
        return "Not enough params"

db.init_app(app)
if __name__ == '__main__':
    port = int(os.environ.get("PORT",80))
    app.run(host='0.0.0.0', port=port, debug=True)
