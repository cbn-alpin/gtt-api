from datetime import datetime

from flask import Blueprint, abort, current_app, jsonify, request

from src.api.auth.services import user_required
from src.api.travel.services import create_travel, delete, get_travel_by_id, get_travels, update

resources = Blueprint("travels", __name__)


# Create a new travel
@resources.route("/user/<int:user_id>/project/<int:project_id>/travels/", methods=["POST"])
@user_required
def post_travel(user_id: int, project_id: int):
    data = request.get_json()
    current_app.logger.debug("In POST /api/user/<int:user_id>/project/<int:project_id>/travels/")
    if data.get("start_date") and data.get("end_date"):
        try:
            if datetime.strptime(data.get("start_date"), "%d/%m/%Y %H:%M:%S") > datetime.strptime(
                data.get("end_date"), "%d/%m/%Y %H:%M:%S"
            ):
                abort(400, description="Start date after end date")
        except ValueError:
            abort(400, description="Invalid date format")

    travel_id = create_travel(user_id, project_id, data)
    return jsonify({"message": "Travel created", "travel_id": travel_id}), 201


# Get all travels of a user
@resources.route("/travels/user/<int:user_id>", methods=["GET"])
@user_required
def get_travels_by_user(user_id: int):
    current_app.logger.info("In GET /api/travels/user/<int:user_id>")
    date_start = request.args.get("date_start")
    date_end = request.args.get("date_end")
    if date_start and date_end:
        if not date_end:
            date_end = datetime.now().strftime("%d/%m/%Y")
        try:
            if datetime.strptime(date_start, "%d/%m/%Y") > datetime.strptime(date_end, "%d/%m/%Y"):
                abort(400, description="Start date after end date")
        except ValueError:
            abort(400, description="Invalid date format")
    response = None
    try:
        response = get_travels(user_id, date_start=date_start, date_end=date_end)
        response = jsonify(response), 200
        return response
    except ValueError as error:
        current_app.logger.error(error)
        response = "Request error", 400
        return response
    except Exception as e:
        current_app.logger.error(e)
        response = (
            "Une erreur est survenue lors de la récupération des données frais de déplacements",
            400,
        )
        return response


@resources.route("/travels/<int:travel_id>/user/<int:user_id>", methods=["PUT"])
@user_required
def update_travel(travel_id: int, user_id: int):
    existing_travel = get_travel_by_id(travel_id)
    print(existing_travel)
    if not existing_travel:
        abort(404, description="Travel not found")
    if existing_travel.get("id_user") != user_id:
        abort(403, description="Unauthorized to update this travel")
    current_app.logger.info(f"In PUT /api/travels/<int:travel_id>")
    posted_data = request.get_json()
    response = update(posted_data, travel_id)
    response = jsonify(response), 200
    return response


@resources.route("/travels/<int:travel_id>/user/<int:user_id>", methods=["DELETE"])
# @user_required
def delete_project(travel_id: int, user_id: int):
    current_app.logger.info("In DELETE /api/travels/<int:travel_id>/user/<int:user_id>")
    try:
        existing_travel = get_travel_by_id(travel_id)
        if existing_travel.get("id_user") != user_id:
            abort(403, description="Unauthorized to update this travel")
        response = delete(travel_id)
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = (
            jsonify({"message": "Une erreur est survenue lors de la suppression du projet"}),
            500,
        )
    finally:
        return response
