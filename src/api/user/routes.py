from flask import Blueprint, abort, current_app, jsonify, request

from src.api.auth.services import admin_required, user_required
from src.api.user.services import (
    create_user,
    delete_user,
    get_user_by_id,
    get_user_projects_by_id,
    get_users,
    update_user,
)

resources = Blueprint("users", __name__)


@resources.route("/user/<int:user_id>/project", methods=["GET"])
@user_required
def get_user_projects(user_id: int):
    current_app.logger.info("In GET /api/user/<int:user_id>/project")
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
@resources.route("/users", methods=["POST"])
@admin_required
def post_user():
    data = request.get_json()

    current_app.logger.debug("In POST /api/users")
    if not data.get("email") or not data.get("first_name") or not data.get("last_name"):
        abort(400, description="Email, First Name, and Last Name are required fields")

    user_id = create_user(data)
    return jsonify({"message": "User created", "user": user_id}), 201


# Get all users
@resources.route("/users", methods=["GET"])
@admin_required
def get_all_users():
    current_app.logger.info("In GET /api/users")
    response = None
    try:
        response = get_users()
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({"message": "An error occurred while retrieving user data"}), 500
    return response


# Get a user by ID
@resources.route("/users/<int:user_id>", methods=["GET"])
@user_required
def get_user_by_id_route(user_id: int):
    current_app.logger.info("In GET /api/users/<int:user_id>")
    response = None
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        response = jsonify(user), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({"message": "An error occurred while retrieving user data"}), 500
    return response


# Update a user by ID
@resources.route("/users/<int:user_id>", methods=["PUT"])
@user_required
def update_user_route(user_id: int):
    current_app.logger.info("In PUT /api/users/<int:user_id>")
    posted_data = request.get_json()
    response = update_user(posted_data, user_id)
    response = jsonify(response), 200
    return response


# Delete a user by ID
@resources.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user_route(user_id: int):
    current_app.logger.info("In DELETE /api/users/<int:user_id>")
    response = None
    try:
        response = delete_user(user_id)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify({"message": "An error occurred while deleting the user"}), 400
    except Exception as e:
        current_app.logger.error(e)
        response = jsonify({"message": "An error occurred while deleting the user"}), 500
    return response
