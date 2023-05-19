#!/usr/bin/python3
"""The City view module"""


from flask import jsonify, abort, make_response, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities')
def fetchiStateCities(state_id):
    """Returns a list of all City objects in JSON format"""
    state = storage.get(State, state_id)
    cities = []
    if not state:
        abort(404)
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>')
def fetchCity(city_id):
    """Retrieves the City with the city_id from the database"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def deleteCity(city_id):
    """Deletes the City with city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def createCity(state_id):
    """Creates a new City under the State with given state_id"""
    state = storage.get(State, state_id)
    cityInfo = request.get_json()
    if not state:
        abort(404)
    if not cityInfo or type(cityInfo) != dict:
        make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'name' not in cityInfo:
        make_response(jsonify({"error": "Missing name"}), 400)

    cityInfo['state_id'] = state_id
    city = City(**cityInfo)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def updateCity(city_id):
    """Updates the City with the given city_id"""
    city = storage.get(City, city_id)
    cityInfo = request.get_json()
    if not city:
        abort(404)
    if not cityInfo or type(cityInfo) != dict:
        make_response(jsonify({"error": "Not a JSON"}), 400)
    ignoredAttr = ['id', 'state_id', 'created_at', 'updated_at']

    for key, value in cityInfo.items():
        if key not in ignoredAttr:
            setattr(city, key, value)
    city.save()

    return make_response(jsonify(city.to_dict()), 200)
