from datetime import datetime

import requests
from flask import Blueprint, abort, current_app, jsonify, request
from flask_jwt_extended import jwt_required

from gtt.api.auth.services import admin_required
from gtt.api.exception import DeleteError, UpdateError
from gtt.api.project.services import (
    create_project,
    delete,
    get_all_projects,
    get_archived_project,
    update,
)
from gtt.api.project.services import get_project_by_id as project_by_id
from gtt.config import get_config

resources = Blueprint("projects", __name__)


@resources.route("/projects", methods=["POST"])
@admin_required
def post_project():
    data = request.get_json()

    current_app.logger.debug("In POST /api/project")
    if not data.get("code") or not data.get("name") or not data.get("start_date"):
        abort(400, description="Code, name and start_date are required fields")

    if data.get("start_date") and data.get("end_date"):
        try:
            if datetime.strptime(data.get("start_date"), "%d/%m/%Y") > datetime.strptime(
                data.get("end_date"), "%d/%m/%Y"
            ):
                abort(400, description="Start date after end date")
        except ValueError:
            abort(400, description="Invalid date format")

    project_id = create_project(data)
    return jsonify({"message": "Project created", "project": project_id}), 201


@resources.route("/projects", methods=["GET"])
@jwt_required()
def get_projects():
    current_app.logger.info("In GET /api/projects")
    response = None
    try:
        response = get_all_projects()
        response = jsonify(response), 200
        return response
    except ValueError as error:
        current_app.logger.error(error)
        response = "Request error", 400
        return response
    except Exception as e:
        current_app.logger.error(e)
        response = "Une erreur est survenue lors de la récupération des données projets", 400
        return response


@resources.route("/projects/archived", methods=["GET"])
@jwt_required()
def get_archived_projects():
    current_app.logger.info("In GET /api/projects/archived")
    response = None
    try:
        response = get_archived_project()
        response = jsonify(response), 200
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = (
            jsonify(
                {"message": "Une erreur est survenue lors de la récupération des données projets"}
            ),
            500,
        )
    finally:
        return response


@resources.route("/projects/<int:project_id>", methods=["GET"])
@jwt_required()
def get_project_by_id(project_id: int):
    current_app.logger.info("In GET /api/projects/<int:project_id>")
    response = None
    try:
        response = project_by_id(project_id)
        response = jsonify(response), 200
        return response
    except ValueError as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    except Exception as e:
        current_app.logger.error(e)
        response = (
            jsonify(
                {"message": "Une erreur est survenue lors de la récupération des données projets"}
            ),
            500,
        )


@resources.route("/projects/<int:project_id>", methods=["PUT"])
@admin_required
def update_project(project_id: int):
    current_app.logger.info("In PUT /api/projects/<int:project_id>")
    posted_data = request.get_json()
    if posted_data.get("start_date") and posted_data.get("end_date"):
        try:
            if datetime.strptime(posted_data.get("start_date"), "%d/%m/%Y") > datetime.strptime(
                posted_data.get("end_date"), "%d/%m/%Y"
            ):
                return "Start date after end date", 400
        except ValueError:
            return "Invalid date format", 400
    try:
        response = update(posted_data, project_id)
    except UpdateError as error:
        return error.message, error.status_code
    except Exception as error:
        return "Error during the modification", 400
    return jsonify(response), 200


@resources.route("/projects/<int:project_id>", methods=["DELETE"])
@admin_required
def delete_project(project_id: int):
    current_app.logger.info("In DELETE /api/projects/<int:project_id>")
    try:
        response = delete(project_id)
        return jsonify(response), 200
    except DeleteError as error:
        current_app.logger.error(error)
        return jsonify(error.args[0]), 403
    except ValueError as error:
        current_app.logger.error(error)
        return (
            jsonify({"message": "Une erreur est survenue lors de la suppression du projet"}),
            error.args[1],
        )
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": "Une erreur est survenue lors de la suppression du projet"}), 500


@resources.route("/projects/gefiproj", methods=["GET"])
@admin_required
def get_gefiproj_project():
    config = get_config()
    url = config.GEFIPROJ_URL

    auth = requests.post(
        f"{url}api/auth/login",
        json={"login": config.GEFIPROJ_LOGIN, "password": config.GEFIPROJ_PASSWORD},
    )
    headers = {"Authorization": f"Bearer {auth.json()['access_token']}"}
    response = requests.get(url=f"{url}api/projects", headers=headers)
    return jsonify(response.json()), 200
