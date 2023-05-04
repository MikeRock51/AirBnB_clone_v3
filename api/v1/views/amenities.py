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


@app_views.route('/amenities', methods=['POST'])
def createAmenity():
    """Creates a new Amenity object"""
    amenityInfo = request.get_json()

    if type(amenityInfo) != dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'name' not in amenityInfo:
        return make_response(jsonify({"error": "Missing name"}), 400)

    amenity = Amenity(**amenityInfo)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updateAmenity(amenity_id):
    """Updates an Amenity object with given amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    amenityInfo = request.get_json()

    if not amenity:
        abort(404)
    if type(amenityInfo) != dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignoredAttr = ['id', 'created_at', 'updated_at']
    for key, value in amenityInfo.items():
        if key not in ignoredAttr:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
