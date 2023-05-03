#!/usr/bin/python3
"""The state view module"""


from models import storage
from api.v1 import app_views


@app_views.route('/states')
def fetchStates():
    """Returns a list of all State objects"""

