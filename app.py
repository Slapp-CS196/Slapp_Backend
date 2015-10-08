import os
from flask import Flask, jsonify, request
from models import db, Slapp
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

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
        return 'Success'
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
        new_slap['radius'] = result.radius
        slapp_list.append(new_slapp)
    return jsonify(slapps=slapp_list)

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
if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    db.init_app(app)
    app.run(host='0.0.0.0', port=port)