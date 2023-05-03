#!/usr/bin/python3
"""The state view module"""


from flask import jsonify, abort, make_response, request
from models import storage
from api.v1.app import app_views
from models.state import State


@app_views.route('/states')
def fetchStates():
    """Returns a list of all State objects in JSON format"""
    allStates = storage.all(State)
    states = []
    for state in allStates.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>')
def fetchState(state_id):
    """Retrieves an instance of a state by state_id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def deleteState(state_id):
    """Deletes the state with id = state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def createState():
    """Creates a new state object"""
    stateInfo = request.get_json()
    if not stateInfo:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in stateInfo:
        return make_response(jsonify({"error": "Missing name"}), 400)

    newState = State(**stateInfo)
    newState.save()
    return make_response(jsonify(newState.to_dict()), 201)
