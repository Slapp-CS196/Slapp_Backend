from flask import Flask, jsonify, request

app = Flask(__name__)

events = [
    {
        "date_detected": 1929,
        "latitude": 40,
        "longitude": 43
    },
    {
        "date_detected": 4934,
        "latitude": 41.56,
        "longitude": 46.89
    },
    {
        "date_detected": 6436,
        "latitude": 47.56,
        "longitude": 46.39
    }
]


@app.route('/api/events', methods=['GET'])
def return_all():
    return jsonify({"events" : events})

@app.route('/api/nearby', methods=['GET'])
def return_nearby():
    returned_events = []
    if 'latitude' and 'longitude' in request.args:
        print request.args['latitude'] + " " + request.args['longitude']
        returned_events = [event for event in events if abs(event['latitude'] - int(request.args['latitude'])) < 1 and abs(event['longitude'] - int(request.args['longitude'])) < 1]
        print returned_events
    return jsonify({"events" : returned_events})

if __name__ == '__main__':
    app.run(debug=True)