from flask import Blueprint, current_app, request, jsonify, abort
from src.api.action.services import create_action

resources = Blueprint('actions', __name__)


# Create a new action
@resources.route('/api/action', methods=['POST'])
def post_action():
    data = request.get_json()

    current_app.logger.debug('In POST /api/action')
    if not data.get('name'):
        abort(400, description="Name are required fields")

    action_id = create_action(data)
    return jsonify({'message': 'Action created', 'action': action_id}), 201






