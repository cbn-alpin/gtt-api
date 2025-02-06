from flask import Blueprint, current_app, request, jsonify, abort
from src.api.action.services import create_action, update

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

@resources.route('/api/actions/<int:action_id>', methods=['PUT'])
def update_action(action_id: int):
    current_app.logger.info(f'In PUT /api/actions/<int:action_id>')
    posted_data = request.get_json()
    response = update(posted_data, action_id)
    response = jsonify(response), 200
    return response




