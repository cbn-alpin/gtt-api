from datetime import datetime
from flask import Blueprint, current_app, request, jsonify, abort
from src.api.project.services import create_project, get_all_projects, update, delete, get_project_by_id as project_by_id
from src.api.userAction.services import create_user_action, delete_user_action_service
from src.models import Project

resources = Blueprint('user_action', __name__)


# Create a new user action
@resources.route('/api/user/action', methods=['POST'])
def post_user_action():
    data = request.get_json()

    current_app.logger.debug('In POST /api/user/action')
    if not data.get('action_id') or not data.get('user_id'):
        abort(400, description="Action ID and User ID are required fields")

    user_action_id = create_user_action(data)
    return jsonify({'message': 'User action created', 'user_action': user_action_id}), 201


@resources.route('/api/user/<int:user_id>/action/<int:action_id>', methods=['DELETE'])
def delete_user_action(user_id: int, action_id: int):
    current_app.logger.info('In DELETE /api/user/<int:user_id>/action/<int:action_id>')
    if type(user_id) != int:
        abort(400, description="User id must be an int")
    if type(action_id) != int:
        abort(400, description="Action id must be an int")
    try:
        response = delete_user_action_service(user_id, action_id)
        return jsonify(response), 204
    except ValueError as error:
        current_app.logger.error(error)
        abort(404, description="User Action not found for given id")
