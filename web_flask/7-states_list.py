#!/usr/bin/python3
"""Starts a flask web application on 0.0.0.0:5000 and lists all states"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def fetchState():
    """Fetches all states instances from storage"""
    allStates = storage.all(State)
    return render_template('7-states_list.html', states=allStates)


@app.teardown_appcontext
def tearDown(self):
    """Removes the current SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
