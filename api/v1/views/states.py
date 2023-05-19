#!/usr/bin/python3
"""The state view module"""


from flask import jsonify, abort, make_response, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def fetchStates():
    """Returns a list of all State objects in JSON format"""
    allStates = storage.all(State)
    states = []
    for state in allStates.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def fetchState(state_id):
    """Retrieves an instance of a state by state_id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['DELETE'])
def deleteState(state_id):
    """Deletes the state with id = state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def createState():
    """Creates a new state object"""
    stateInfo = request.get_json()
    if not stateInfo or type(stateInfo) != dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in stateInfo:
        return make_response(jsonify({"error": "Missing name"}), 400)

    newState = State(**stateInfo)
    newState.save()
    return make_response(jsonify(newState.to_dict()), 201)


@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['PUT'])
def updateState(state_id):
    """Updates the state with the specified state_id"""
    state = storage.get(State, state_id)
    stateInfo = request.get_json()
    if not state:
        abort(404)
    elif not stateInfo or type(stateInfo) != dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignoredAttr = ['id', 'created_at', 'updated_at']
    for key, value in stateInfo.items():
        if key not in ignoredAttr:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
