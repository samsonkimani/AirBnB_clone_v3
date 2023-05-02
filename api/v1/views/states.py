#!/usr/bin/python3
"""model - states """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ get the list of all states"""
    all_states = storage.all(State).values()
    states = []
    for state in all_states:
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """ function to retrieve the state by id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a state using the state id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ creating a new state"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    new_instance = State(**data)
    new_instance.save()
    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def edit_state(state_id):
    """ edit the state_id """
    state = storage.get(State, state_id)

    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
