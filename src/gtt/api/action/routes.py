from flask import Blueprint, abort, current_app, jsonify, request

from gtt.api.action.services import create_action, delete, update
from gtt.api.auth.services import admin_required

resources = Blueprint("actions", __name__)


# Create a new action
@resources.route("/actions", methods=["POST"])
@admin_required
def post_action():
    data = request.get_json()

    current_app.logger.debug("In POST /api/actions")
    if not data.get("name"):
        abort(400, description="name field is missing")

    action_id = create_action(data)
    return jsonify({"message": "Action created", "action_id": action_id}), 201


@resources.route("/actions/<int:action_id>", methods=["PUT"])
@admin_required
def update_action(action_id: int):
    current_app.logger.info("In PUT /api/actions/<int:action_id>")
    posted_data = request.get_json()
    response = update(posted_data, action_id)
    response = jsonify(response), 200
    return response


@resources.route("/actions/<int:action_id>", methods=["DELETE"])
@admin_required
def delete_action(action_id: int):
    current_app.logger.info("In DELETE /api/actions/<int:action_id>")
    response = delete(action_id)
    return jsonify(response), 200
