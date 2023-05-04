#!/usr/bin/python3
"""The places views module"""

from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places')
def fetchPlaces(city_id):
    """Retrieves all Places of a City from storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>')
def fetchPlace(place_id):
    """Retrieves the Place with the place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def deletePlace(place_id):
    """Deletes the Place object with given place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def createPlace(city_id):
    """Creates a new place under the city with city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    placeInfo = request.get_json()
    if type(placeInfo) != dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'user_id' not in placeInfo:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif not storage.get(User, placeInfo.get('user_id')):
        abort(404)
    elif 'name' not in placeInfo:
        return make_response(jsonify({"error": "Missing name"}), 400)
    placeInfo['city_id'] = city_id
    place = Place(**placeInfo)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def updatePlace(place_id):
    """Updates the Place object with the place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    placeInfo = request.get_json()
    if type(placeInfo) != dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignoredKeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in placeInfo.items():
        if key not in ignoredKeys:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
