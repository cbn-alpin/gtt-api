from flask import Blueprint, current_app, request, jsonify, abort
from src.models import User
from src.api.user.services import create_user, get_user_projects_by_id, get_users, update_user, delete_user, get_user_by_id

resources = Blueprint('users', __name__)


@resources.route('/api/user/<int:user_id>/project', methods=['GET'])
def get_user_projects(user_id: int):
    current_app.logger.info('In GET /api/user/<int:user_id>/project')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    try:
        response = get_user_projects_by_id(user_id=user_id, date_start=date_start, date_end=date_end)
        return jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        raise error
    except Exception as e:
        current_app.logger.error(e)
        raise e


