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

