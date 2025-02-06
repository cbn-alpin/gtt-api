from enum import Enum

from flask import abort, current_app, json
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
import sqlalchemy
from src.api import db

from src.api.userActionTime.schema import ProjectTimeSchema, ActionTimeSchema
from src.api.exception import DBInsertException, NotFoundError
from src.models import Action, Project, User, UserAction, UserActionTime


def get_user_projects_time_by_id(user_id: int, date_start: str, date_end: str):
    projects_actions_tuple = db.session.query(Project, UserActionTime).select_from(UserActionTime) \
        .join(Action, UserActionTime.id_action == Action.id_action) \
        .join(Project, Action.id_project == Project.id_project) \
        .filter(UserActionTime.date.between(date_start, date_end)) \
        .filter(UserActionTime.id_user == user_id).all()
    if not projects_actions_tuple:
        raise NotFoundError("No projects found for the given user and date range")

    list_projects = []
    for project_action in projects_actions_tuple:
        project_object, action_object = project_action
        project = ProjectTimeSchema().dump(project_object)
        action = ActionTimeSchema().dump(action_object)
        existing_project = next((p for p in list_projects if p["id_project"] == project["id_project"]), None)
        if existing_project:
            existing_action = next((a for a in existing_project["list_action"] if a["id_action"] == action["id_action"]), None)
            if existing_action:
                existing_action["list_time"].append({"date": action["date"], "duration": action["duration"]})
            else:
                action["list_time"] = [{"date": action["date"], "duration": action["duration"]}]
                existing_project["list_action"].append(action)
        else:
            action["list_time"] = [{"date": action["date"], "duration": action["duration"]}]
            project["list_action"] = [action]
            list_projects.append(project)

    db.session.close()
    return list_projects
