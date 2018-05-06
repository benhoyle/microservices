"""Routes for User Services as part of Users Blueprint."""
# services/users/project/api/users.py

from flask import Blueprint, jsonify

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    """Test ping function."""
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
