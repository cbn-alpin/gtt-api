from datetime import datetime

from flask import Blueprint, abort, current_app, jsonify, request

from src.api.auth.services import user_required
from src.api.userActionTime.services import (
    create_or_update_user_action_time,
    get_user_project_actions_time_entries,
    get_user_projects_time_by_id,
)
from src.models import User

resources = Blueprint("users_action_time", __name__)


@resources.route("/user/<int:user_id>/projects/times", methods=["GET"])
@user_required
def get_user_projects(user_id: int):
    current_app.logger.info("In GET /api/user/<int:user_id>/project")
    date_start = request.args.get("date_start")
    date_end = request.args.get("date_end")
    if not date_start or not date_end:
        abort(400, description="Both 'date_start' and 'date_end' must be provided.")
    try:
        datetime.strptime(date_start, "%Y-%m-%d")
        datetime.strptime(date_end, "%Y-%m-%d")
    except ValueError:
        abort(400, description="Invalid date format. Please use YYYY-MM-DD.")

    try:
        response = get_user_projects_time_by_id(
            user_id=user_id, date_start=date_start, date_end=date_end
        )
        return jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        raise error
    except Exception as e:
        current_app.logger.error(e)
        raise e


@resources.route("/user/<int:user_id>/projects/times", methods=["POST"])
@user_required
def post_put_user_time(user_id: int):
    data = request.get_json()
    current_app.logger.debug("In POST /api/user/<int:user_id>/projects/times")
    if data.get("duration", None) == None or not data.get("date"):
        abort(400, description="duration and date are required fields")

    action_id = create_or_update_user_action_time(
        data.get("date"), data.get("duration"), user_id, data.get("id_action")
    )
    return jsonify({"message": "time saved", "action": action_id}), 201


@resources.route("/project/<int:project_id>/actions", methods=["GET"])
def get_project_actions_time_entries(project_id):
    try:
        response = get_user_project_actions_time_entries(project_id)
        return jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        raise error
    except Exception as e:
        current_app.logger.error(e)
        raise e
