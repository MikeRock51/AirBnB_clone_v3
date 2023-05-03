#!/usr/bin/python3
"""Starts a Flask app on 0.0.0.0:5000"""

from flask import Flask, render_template, abort
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def fetchStates():
    """Returns a page with all states in storage"""
    states = storage.all(State)

    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def fetchStateInstance(id):
    """Returns a page with requested state and it's cities"""
    states = storage.all(State)
    select = None

    for state in states.values():
        if state.id == id:
            select = state
            break
    if not select:
        abort(404)
    return render_template('9-states.html', state=select)


@app.teardown_appcontext
def tearDown(self):
    """Removes the current SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
