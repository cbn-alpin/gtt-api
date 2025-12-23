from flask import Blueprint, abort, current_app, jsonify, request

from src.api.action.services import create_action, delete, update
from src.api.auth.services import admin_required

resources = Blueprint("actions", __name__)


# Create a new action
@resources.route("/api/actions", methods=["POST"])
@admin_required
def post_action():
    data = request.get_json()

    current_app.logger.debug("In POST /api/actions")
    if not data.get("name"):
        abort(400, description="name field is missing")

    action_id = create_action(data)
    return jsonify({"message": "Action created", "action_id": action_id}), 201


@resources.route("/api/actions/<int:action_id>", methods=["PUT"])
@admin_required
def update_action(action_id: int):
    current_app.logger.info("In PUT /api/actions/<int:action_id>")
    posted_data = request.get_json()
    response = update(posted_data, action_id)
    response = jsonify(response), 200
    return response


@resources.route("/api/actions/<int:action_id>", methods=["DELETE"])
@admin_required
def delete_action(action_id: int):
    current_app.logger.info("In DELETE /api/actions/<int:action_id>")
    try:
        response = delete(action_id)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = (
            jsonify({"message": "Une erreur est survenue lors de la suppression de l'action"}),
            500,
        )
    finally:
        return response
