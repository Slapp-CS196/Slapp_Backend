from flask import Flask, jsonify, request
from models import db, Slapp
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

@app.route('/api/new', methods=['GET'])
def create_new():
    if 'user_id' and 'time' and 'latitude' and 'longitude' in request.args:
        user_id = request.args['user_id']
        time = request.args['time']
        latitude = request.args['latitude']
        longitude = request.args['longitude']
        slapp = Slapp(user_id, time, latitude, longitude)
        db.session.add(slapp)
        db.session.commit()
        return 'Success'
    else:
        return 'Error, not enough parameters'

@app.route('/api/slapps', methods=['GET'])
def return_all():
    slapps = Slapp.query.all()
    return slapps

# @app.route('/api/nearby', methods=['GET'])
# def return_nearby():
#     returned_events = []
#     if 'latitude' and 'longitude' and 'time' in request.args:
#         print request.args['latitude'] + " " + request.args['longitude']
#         returned_events = [event for event in events if abs(event['latitude'] - int(request.args['latitude'])) < 1 and abs(event['longitude'] - int(request.args['longitude'])) < 1]
#         print returned_events
#     return jsonify({"events" : returned_events})

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)