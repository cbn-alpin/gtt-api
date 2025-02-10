from datetime import datetime
from enum import Enum
from sqlalchemy import and_, func, literal_column
from flask import abort, current_app, json
from flask_sqlalchemy import SQLAlchemy
from marshmallow import EXCLUDE
import sqlalchemy
from src.api import db

from src.api.userActionTime.schema import ActionWithTimeSchema, ProjectTimeSchema, ActionTimeSchema
from src.api.exception import DBInsertException, NotFoundError
from src.models import Action, Project, User, UserAction, UserActionTime

def create_or_update_user_action_time(date: str, duration: float, id_user: int, id_action: int):  
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
    date_series = (
        db.session.query(
            func.generate_series(
                literal_column(f"'{date_start}'::timestamp"),
                literal_column(f"'{date_end}'::timestamp"),
                '1 day'
            ).label('date')
        ).subquery()
    )

    projects_actions_time_tuple = db.session.query(Project, Action, date_series.c.date,
            func.coalesce(func.sum(UserActionTime.duration), 0) \
        .label('duration')) \
        .join(Action, Project.id_project == Action.id_project)\
        .join(UserAction, Action.id_action == UserAction.id_action)\
        .join(date_series, literal_column('1=1'))\
        .outerjoin( UserActionTime,
            and_(UserActionTime.id_action == Action.id_action,
                func.date(UserActionTime.date) == func.date(date_series.c.date)))\
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
        )\
        .filter(UserAction.id_user == user_id).all()
    if not projects_actions_time_tuple:
        raise NotFoundError("No projects found for the given user and date range")

    list_projects = []
    for project_action_time in projects_actions_time_tuple:
        project_object, action_object, action_time_date, action_time_duration = project_action_time
        project = ProjectTimeSchema().dump(project_object)
        action = ActionWithTimeSchema().dump(action_object)
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



def get_total_duration_action(user_id: int, year: int):
    today = datetime.today()
    date_start = f"{year}-01-01"
    date_end = today.strftime("%Y-%m-%d") if today.year == year and today.day != 31 else f"{year}-12-31"

    total_durations = db.session.query(
        Project.id_project,
        Project.name.label("project_name"),
        Action.id_action,
        Action.name.label("action_name"),
        func.coalesce(func.sum(UserActionTime.duration), 0).label("total_duration")
    ).join(Action, Project.id_project == Action.id_project) \
    .join(UserAction, Action.id_action == UserAction.id_action) \
    .outerjoin(UserActionTime, 
        and_(UserActionTime.id_action == Action.id_action,
             func.date(UserActionTime.date) >= date_start,
             func.date(UserActionTime.date) <= date_end)
    ) \
    .filter(UserAction.id_user == user_id) \
    .group_by(Project.id_project, Project.name, Action.id_action, Action.name) \
    .order_by(Project.id_project, Action.id_action) \
    .all()

    if not total_durations:
        raise NotFoundError("No projects found for the given user and year")

    results = []
    for project_id, project_name, action_id, action_name, total_duration in total_durations:
        project = next((p for p in results if p["id_project"] == project_id), None)
        if project:
            project["list_action"].append({
                "id_action": action_id,
                "action_name": action_name,
                "total_duration": total_duration
            })
        else:
            results.append({
                "id_project": project_id,
                "project_name": project_name,
                "list_action": [{
                    "id_action": action_id,
                    "action_name": action_name,
                    "total_duration": total_duration
                }]
            })

    db.session.close()
    return results