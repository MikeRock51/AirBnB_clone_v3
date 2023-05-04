#!/usr/bin/python3
"""The places views module"""

from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews')
def fetchPlaceReviews(place_id):
    """Returns a list of all Reviews of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>')
def fetchReview(review_id):
    """Retrieves a review object based on the review_id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def deleteReview(review_id):
    """Deletes the Review object with the review_id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def createReview(place_id):
    """Creates a Review object under the Place with place_id"""
    if not storage.get(Place, place_id):
        abort(404)
    reviewInfo = request.get_json()
    if type(reviewInfo) != dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'user_id' not in reviewInfo.keys():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    elif not storage.get(User, reviewInfo['user_id']):
        abort(404)
    elif 'text' not in reviewInfo.keys():
        return make_response(jsonify({"error": "Missing text"}), 400)
    reviewInfo['place_id'] = place_id
    review = Review(**reviewInfo)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updateReview(review_id):
    """Updates the Review object with review_id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    reviewInfo = request.get_json()
    if type(reviewInfo) != dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignoredKeys = ['id, user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in reviewInfo.items():
        if key not in ignoredKeys:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
