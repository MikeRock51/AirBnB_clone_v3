#!/usr/bin/python3
'''A flask web app that runs on 0.0.0.0:5000'''

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": '0.0.0.0'}})


@app.teardown_appcontext
def tearDown(self):
    """Removes the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def notFound(error):
    """Returns a JSON formatted not found response"""
    return make_response(jsonify({'error': 'Not found'}))


if __name__ == '__main__':
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'

    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = 5002

    app.run(debug=True, host=host, port=port, threaded=True)
