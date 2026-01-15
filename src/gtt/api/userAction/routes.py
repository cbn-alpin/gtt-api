from flask import Blueprint, abort, current_app, jsonify

from gtt.api.auth.services import user_required
from gtt.api.userAction.services import create_user_action, delete_user_action_service

resources = Blueprint("user_action", __name__)


# Create a new user action
@resources.route("/user/<int:user_id>/action/<int:action_id>", methods=["POST"])
@user_required
def post_user_action(user_id: int, action_id: int):
    if type(user_id) != int:
        abort(400, description="User id must be an int")
    if type(action_id) != int:
        abort(400, description="Action id must be an int")

    current_app.logger.debug("In POST /api/user/action")

    user_action_id = create_user_action(user_id, action_id)
    return jsonify({"message": "User action created", "user_action": user_action_id}), 201


@resources.route("/user/<int:user_id>/action/<int:action_id>", methods=["DELETE"])
@user_required
def delete_user_action(user_id: int, action_id: int):
    current_app.logger.info("In DELETE /api/user/<int:user_id>/action/<int:action_id>")
    if type(user_id) is not int:
        abort(400, description="User id must be an int")
    if type(action_id) is not int:
        abort(400, description="Action id must be an int")
    try:
        response = delete_user_action_service(user_id, action_id)
        return jsonify(response), 204
    except ValueError as error:
        current_app.logger.error(error)
        abort(404, description="User Action not found for given id")
