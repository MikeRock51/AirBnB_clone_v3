#!/usr/bin/python3
"""The places views module"""

from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


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
