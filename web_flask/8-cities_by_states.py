#!/usr/bin/python3
"""Starts a flask web application on 0.0.0.0:5000
and lists all cities by state
"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def fetchCities():
    """Returns a page that lists all cities by state"""
    states = storage.all(State)
    stateCities = {}

    for state in states.values():
        stateCities[state] = state.cities

    return render_template('8-cities_by_states.html', stateCities=stateCities)


@app.teardown_appcontext
def tearDown(self):
    """Removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
