from enum import Enum
import hashlib

from flask import abort, current_app, json
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
import sqlalchemy
from src.api import db

from src.api.action.schema import ActionSchema
from src.api.exception import DBInsertException
from src.api.project.schema import ProjectSchema
from src.api.user.schema import UserInputSchema, UserSchema
from src.models import Action, Project, User, UserAction


def get_user_projects_by_id(user_id: int):
    projects_actions_tuple = db.session.query(Project, Action).join(Action).join(UserAction).filter(UserAction.id_user == user_id).all()

    list_projects = []
    for project_action in projects_actions_tuple:
        project_object, action_object = project_action
        project = ProjectSchema().dump(project_object)
        action = ActionSchema().dump(action_object)
        existing_project = next((p for p in list_projects if p["id_project"] == project["id_project"]), None)
        if existing_project:
            existing_project["list_action"].append(action)
        else:
            project["list_action"] = [action]
            list_projects.append(project)

    db.session.close()
    return list_projects


def create_user(data: dict) -> int:
    try:
        user_data = UserInputSchema().load(data)

        user = User(
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_admin=user_data.get('is_admin', False),
            password=hashlib.md5(user_data["password"].encode('utf-8')).hexdigest()
        )

        db.session.add(user)
        db.session.commit()
        return user.id_user

    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"UserDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()
    except sqlalchemy.exc.IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"UserDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()


def get_users():
    users = []
    try:
        users_objects = db.session.query(User)
        users = [UserSchema().dump(user) for user in users_objects]
        db.session.close()
        return users
    except ValueError as error:
        current_app.logger.error(f"UserDBService - get_all_users : {error}")
        raise
    finally:
        if db.session is not None:
            db.session.close()


def update_user(data, user_id):
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        abort(404, description="User not found")

    user = UserInputSchema().load(data)

    if user.get("is_admin", False) and not existing_user.is_admin :
        abort(403, description="Forbiden, can't change the role to admin")

    if user.get("password", False):
        user["password"] = hashlib.md5(user["password"].encode('utf-8')).hexdigest()

    db.session.query(User).filter_by(id_user=user_id).update(user)
    db.session.commit()
    db.session.close()
    return get_user_by_id(user_id)


def delete_user(user_id: int):
    try:
        db.session.query(User).filter_by(id_user=user_id).delete()
        db.session.commit()

        db.session.close()
        return {'message': f'Le user \'{user_id}\' a été supprimé'}
    except Exception as error:
        db.session.rollback()
        current_app.logger.error(f"UserDBService - delete : {error}")
        raise
    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"UserDBService - delete : {error}")
        raise
    finally:
        if db.session is not None:
            db.session.close()


def get_user_by_id(user_id: int):
    user_object = db.session.query(User).filter_by(id_user=user_id).first()
    db.session.close()
    return user_object.email


