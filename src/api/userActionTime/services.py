from datetime import datetime
from enum import Enum
from sqlalchemy import and_, func, literal_column
from flask import abort, current_app, json
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
import sqlalchemy
from src.api import db
from datetime import datetime
from src.api.userActionTime.schema import ActionWithTimeSchema, ProjectTimeSchema, ActionTimeSchema
from src.api.exception import DBInsertException, NotFoundError
from src.models import Action, Project, User, UserAction, UserActionTime
from sqlalchemy import func, literal_column, and_

def create_or_update_user_action_time(date: str, duration: float, id_user: int, id_action: int):  
    if duration >= 0 or duration <= 24:
        abort(400, description="La durée doit être comprise entre 0 et 24 heures.")
    existing_entry = db.session.query(UserActionTime).filter_by(
        id_user=id_user,
        id_action=id_action,
        date=datetime.strptime(date, "%Y-%m-%d").date()
    ).first()

    if existing_entry:
        existing_entry.duration = duration  
    else:
        new_entry = UserActionTime(
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            duration=duration,
            id_user=id_user,
            id_action=id_action
        )
        db.session.add(new_entry)

    db.session.commit()
    return id_action






def get_user_projects_time_by_id(user_id: int, date_start: str, date_end: str):
    start_year = datetime.strptime(date_start, '%Y-%m-%d').year
    end_year = datetime.strptime(date_end, '%Y-%m-%d').year

    if start_year != end_year:
        raise ValueError("Start and end dates must belong to the same year.")
    
    date_series = (
        db.session.query(
            func.generate_series(
                literal_column(f"'{start_year}-01-01'::timestamp"),
                literal_column(f"'{start_year}-12-31'::timestamp"),
                '1 day'
            ).label('date')
        ).subquery()
    )

    projects_actions_time_tuple = db.session.query(
        Project, Action, date_series.c.date,
        func.coalesce(func.sum(UserActionTime.duration), 0).label('duration')
    ) \
    .join(Action, Project.id_project == Action.id_project) \
    .join(UserAction, Action.id_action == UserAction.id_action) \
    .join(date_series, literal_column('1=1')) \
    .outerjoin(UserActionTime,
        and_(UserActionTime.id_action == Action.id_action,
             func.date(UserActionTime.date) == func.date(date_series.c.date))
    ) \
    .group_by(
        Project.id_project,
        Project.name,
        Action.id_action,
        Action.name,
        date_series.c.date
    ) \
    .order_by(
        Project.id_project,
        Action.id_action,
        date_series.c.date
    ) \
    .filter(UserAction.id_user == user_id,
            func.date(date_series.c.date) >= func.date(date_start),
            func.date(date_series.c.date) <= func.date(date_end)) \
    .all()

    if not projects_actions_time_tuple:
        raise NotFoundError("No projects found for the given user and date range")

    total_duration_per_action = db.session.query(
        Action.id_action,
        func.coalesce(func.sum(UserActionTime.duration), 0).label("total_duration")
    ) \
    .join(UserAction, Action.id_action == UserAction.id_action) \
    .outerjoin(UserActionTime,
        and_(UserActionTime.id_action == Action.id_action,
             func.date(UserActionTime.date) >= f'{start_year}-01-01',
             func.date(UserActionTime.date) <= f'{start_year}-12-31')
    ) \
    .filter(UserAction.id_user == user_id) \
    .group_by(Action.id_action) \
    .all()

    total_duration_map = {action_id: total_duration for action_id, total_duration in total_duration_per_action}

    list_projects = []
    for project_action_time in projects_actions_time_tuple:
        project_object, action_object, action_time_date, action_time_duration = project_action_time
        project = ProjectTimeSchema().dump(project_object)
        action = ActionWithTimeSchema().dump(action_object)
        action["total_duration"] = total_duration_map.get(action["id_action"], 0)

        existing_project = next((p for p in list_projects if p["id_project"] == project["id_project"]), None)
        if existing_project:
            existing_action = next((a for a in existing_project["list_action"] if a["id_action"] == action["id_action"]), None)
            if existing_action:
                existing_action["list_time"].append({"date": action_time_date, "duration": action_time_duration})
            else:
                action["list_time"] = [{"date": action_time_date, "duration": action_time_duration}]
                existing_project["list_action"].append(action)
        else:
            action["list_time"] = [{"date": action_time_date, "duration": action_time_duration}]
            project["list_action"] = [action]
            list_projects.append(project)

    db.session.close()
    return list_projects




  