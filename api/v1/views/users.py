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


@app_views.route('/users', methods=['POST'])
def createUser():
    """Creates a new User object"""
    userInfo = request.get_json()
    if type(userInfo) != dict:
        make_response(jsonify({"error": "Not a JSON"}), 400)
    elif 'email' not in userInfo:
        return make_response(jsonify({"error": "Missing email"}), 400)
    elif 'password' not in userInfo:
        return make_response(jsonify({"error": "Missing password"}), 400)

    user = User(**userInfo)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def updateUser(user_id):
    """Updates a User object with given user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    userInfo = request.get_json()
    if type(userInfo) != dict:
        make_response(jsonify({"error": "Not a JSON"}), 400)
    ignoredKeys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in userInfo.items():
        if key not in ignoredKeys:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
