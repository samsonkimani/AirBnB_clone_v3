#!/usr/bin/python3
"""module - index file"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_code():
    """return status code"""
    return jsonify({"status": "OK"})
