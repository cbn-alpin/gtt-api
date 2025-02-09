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


@resources.route('/api/user/action/<int:user_action_id>', methods=['DELETE'])
def delete_user_action(user_action_id: int):
    current_app.logger.info('In DELETE /api/user/actions/<int:user_action_id>')
    try:
        response = delete_user_action_service(user_action_id)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'An error occurred while deleting the user action'}), 500
    finally:
        return response
