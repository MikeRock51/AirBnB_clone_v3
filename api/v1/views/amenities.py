#!/usr/bin/python3
"""Amenity views module"""

from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
def fetchAmenities():
    """Retrieves the list of all amenities in storage"""
    allAmenities = storage.all(Amenity)
    amenities = []
    for amenity in allAmenities.values():
        amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>')
def getAmenity(amenity_id):
    """Retrieves a single Amenity with the amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def deleteAmenity(amenity_id):
    """Deletes the Amenity with the given amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    return make_response(jsonify({}), 200)
