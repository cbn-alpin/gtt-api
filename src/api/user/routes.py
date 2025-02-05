from flask import Blueprint, current_app, request, jsonify, abort
from src.models import User
from src.api.user.services import create_user, get_user_projects_by_id, get_users, update_user, delete_user, get_user_by_id

resources = Blueprint('users', __name__)


@resources.route('/api/user/<int:user_id>/project', methods=['GET'])
def get_user_projects(user_id: int):
    current_app.logger.info('In GET /api/user/<int:user_id>/project')
    try:
        response = get_user_projects_by_id(user_id)
        return jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        raise error
    except Exception as e:
        current_app.logger.error(e)
        raise e


# Create a new user
@resources.route('/api/users', methods=['POST'])
def post_user():
    data = request.get_json()

    current_app.logger.debug('In POST /api/users')
    if not data.get('email') or not data.get('first_name') or not data.get('last_name'):
        abort(400, description="Email, First Name, and Last Name are required fields")

    user_id = create_user(data)
    return jsonify({'message': 'User created', 'user': user_id}), 201


# Get all users
@resources.route('/api/users', methods=['GET'])
def get_all_users():
    current_app.logger.info('In GET /api/users')
    response = None
    try:
        response = get_users()
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'An error occurred while retrieving user data'}), 500
    finally:
        return response


# Get a user by ID
@resources.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id_route(user_id: int):
    current_app.logger.info('In GET /api/users/<int:user_id>')
    response = None
    try:
        response = get_user_by_id(user_id)
        response = jsonify(response), 200
        return response
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'An error occurred while retrieving user data'}), 500


# Update a user by ID
@resources.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user_route(user_id: int):
    current_app.logger.info(f'In PUT /api/users/<int:user_id>')
    posted_data = request.get_json()
    response = update_user(posted_data, user_id)
    response = jsonify(response), 200
    return response


# Delete a user by ID
@resources.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id: int):
    current_app.logger.info('In DELETE /api/users/<int:user_id>')
    try:
        response = delete_user(user_id)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({'message': 'An error occurred while deleting the user'}), 500
    finally:
        return response
