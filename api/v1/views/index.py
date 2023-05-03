#!/usr/bin/python3
"""Index module file"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def statusOk():
    """Returns a json formatted OK status"""
    return jsonify({"status": "OK"})
