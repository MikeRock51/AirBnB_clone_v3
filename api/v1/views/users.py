#!/usr/bin/python3
"""The users views module"""

from flask import make_response, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users')
def fetchUsers():
    """Retrieves a list of all users from storage"""
    allUsers = storage.all(User)
    users = []
    for user in allUsers.values():
        users.append(user.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>')
def fetchUser(user_id):
    """Retrieves the user with the given user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    """Deletes the user with given user_id from storage"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    return make_response(jsonify({}), 200)
