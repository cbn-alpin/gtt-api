from datetime import datetime

from flask import abort
from sqlalchemy import and_, func, literal_column, or_

from gtt.api.exception import NotFoundError
from gtt.api.userActionTime.schema import ActionWithTimeSchema, ProjectTimeSchema
from gtt.database import db
from gtt.models import Action, Project, User, UserAction, UserActionTime


def create_or_update_user_action_time(date: str, duration: float, id_user: int, id_action: int):
    if duration < 0 or duration > 24:
        abort(400, description="Duration must be between 0 and 24.")
    existing_entry = (
        db.session.query(UserActionTime)
        .filter_by(
            id_user=id_user, id_action=id_action, date=datetime.strptime(date, "%Y-%m-%d").date()
        )
        .first()
    )

    if existing_entry:
        existing_entry.duration = duration
    else:
        new_entry = UserActionTime(
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            duration=duration,
            id_user=id_user,
            id_action=id_action,
        )
        db.session.add(new_entry)

    db.session.commit()
    return id_action


def get_user_projects_time_by_id(user_id: int, date_start: str, date_end: str):
    date_series = db.session.query(
        func.generate_series(
            literal_column(f"'{date_start}'::timestamp"),
            literal_column(f"'{date_end}'::timestamp"),
            "1 day",
        ).label("date")
    ).subquery()

    projects_actions_time_tuple = (
        db.session.query(
            Project,
            Action,
            date_series.c.date,
            func.coalesce(func.sum(UserActionTime.duration), 0).label("duration"),
        )
        .join(Action, Project.id_project == Action.id_project)
        .join(UserAction, Action.id_action == UserAction.id_action)
        .join(date_series, literal_column("1=1"))
        .outerjoin(
            UserActionTime,
            and_(
                UserActionTime.id_action == Action.id_action,
                func.date(UserActionTime.date) == func.date(date_series.c.date),
            ),
        )
        .group_by(
            Project.id_project, Project.name, Action.id_action, Action.name, date_series.c.date
        )
        .order_by(Project.id_project, Action.id_action, date_series.c.date)
        .filter(
            UserAction.id_user == user_id,
            or_(UserActionTime.id_user == user_id, UserActionTime.id_user == None),
            func.date(date_series.c.date) >= func.date(date_start),
            func.date(date_series.c.date) <= func.date(date_end),
        )
        .all()
    )

    if not projects_actions_time_tuple:
        raise NotFoundError("No projects found for the given user and date range")

    total_duration_per_action = (
        db.session.query(
            Action.id_action,
            func.coalesce(func.sum(UserActionTime.duration), 0).label("total_duration"),
        )
        .join(UserAction, Action.id_action == UserAction.id_action)
        .outerjoin(
            UserActionTime,
            and_(
                UserActionTime.id_action == Action.id_action,
                or_(UserActionTime.id_user == user_id, UserActionTime.id_user == None),
                func.date(UserActionTime.date) >= func.date(date_start),
                func.date(UserActionTime.date) <= func.date(date_end),
            ),
        )
        .filter(UserAction.id_user == user_id)
        .group_by(Action.id_action)
        .all()
    )

    total_duration_map = {
        action_id: total_duration for action_id, total_duration in total_duration_per_action
    }

    list_projects = []
    for project_action_time in projects_actions_time_tuple:
        project_object, action_object, action_time_date, action_time_duration = project_action_time
        project = ProjectTimeSchema().dump(project_object)
        action = ActionWithTimeSchema().dump(action_object)
        action["total_duration"] = total_duration_map.get(action["id_action"], 0)

        existing_project = next(
            (p for p in list_projects if p["id_project"] == project["id_project"]), None
        )
        if existing_project:
            existing_action = next(
                (
                    a
                    for a in existing_project["list_action"]
                    if a["id_action"] == action["id_action"]
                ),
                None,
            )
            if existing_action:
                existing_action["list_time"].append(
                    {"date": action_time_date, "duration": action_time_duration}
                )
            else:
                action["list_time"] = [{"date": action_time_date, "duration": action_time_duration}]
                existing_project["list_action"].append(action)
        else:
            action["list_time"] = [{"date": action_time_date, "duration": action_time_duration}]
            project["list_action"] = [action]
            list_projects.append(project)

    return list_projects


def get_user_project_actions_time_entries(project_id):
    project = db.session.query(Project).filter(Project.id_project == project_id).first()

    if not project:
        return None

    response = {
        "id_project": project.id_project,
        "name_project": project.name,
        "numero_project": project.code,
        "time_entries": [],
    }

    actions = db.session.query(Action).filter(Action.id_project == project_id).all()
    for action in actions:
        time_entries = (
            db.session.query(UserActionTime)
            .filter(UserActionTime.id_action == action.id_action)
            .all()
        )
        for time_entry in time_entries:
            user = db.session.query(User).filter(User.id_user == time_entry.id_user).first()
            if user:
                response["time_entries"].append(
                    {
                        "id_user": user.id_user,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "numero_action": action.numero_action,
                        "name_action": action.name,
                        "date": time_entry.date.strftime("%Y-%m-%d"),
                        "duration": float(time_entry.duration),
                    }
                )

    return response
