from datetime import datetime, timedelta

import sqlalchemy
from flask import current_app

from src.api.exception import DBInsertException
from src.api.expense.schema import ExpenseSchema
from src.api.travel.schema import TravelPutSchema, TravelSchema
from src.database import db
from src.models import Expense, Project, Travel


def create_travel(user_id, project_id, travel_data: dict) -> int:
    try:
        schema = TravelSchema()
        travel = schema.load(travel_data)

        new_travel = Travel(
            status=travel["status"],
            start_date=travel.get("start_date"),
            end_date=travel.get("end_date"),
            start_place=travel.get("start_place"),
            return_place=travel.get("return_place"),
            purpose=travel.get("purpose"),
            start_municipality=travel.get("start_municipality"),
            end_municipality=travel.get("end_municipality"),
            night_municipality=travel.get("night_municipality"),
            destination=travel.get("destination"),
            night_count=travel.get("night_count"),
            meal_count=travel.get("meal_count"),
            comment=travel.get("comment"),
            license_vehicle=travel.get("license_vehicle"),
            comment_vehicle=travel.get("comment_vehicle"),
            start_km=travel.get("start_km"),
            end_km=travel.get("end_km"),
            id_user=user_id,
            id_project=project_id,
        )

        db.session.add(new_travel)
        db.session.commit()
        return new_travel.id_travel

    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"travelDBService - insert : {error}")
        raise DBInsertException() from error

    except sqlalchemy.exc.IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"travelDBService - insert : {error}")
        raise DBInsertException() from error


def get_travels(user_id, date_start: str = None, date_end: str = None):
    query = db.session.query(Travel, Expense, Project.id_project, Project.code)
    query = query.outerjoin(Expense, Travel.id_travel == Expense.id_travel)
    query = query.outerjoin(Project, Travel.id_project == Project.id_project)
    query = query.filter(Travel.id_user == user_id)

    if date_start:
        query = query.filter(Travel.start_date >= datetime.strptime(date_start, "%d/%m/%Y"))
    if date_end:
        end_date = datetime.strptime(date_end, "%d/%m/%Y")
        end_date = end_date + timedelta(days=1)
        query = query.filter(Travel.end_date <= end_date)

    travels_expenses_tuple = query.all()

    list_travels = []
    for travel, expense, id_project, project_code in travels_expenses_tuple:
        travel_data = TravelSchema().dump(travel)
        expense_data = ExpenseSchema().dump(expense) if expense else None

        travel_data["id_project"] = id_project
        travel_data["project_code"] = project_code

        existing_travel = next(
            (t for t in list_travels if t["id_travel"] == travel_data["id_travel"]), None
        )

        if existing_travel:
            if expense_data:
                existing_travel["list_expenses"].append(expense_data)
                existing_travel["total_expense"] += expense_data["amount"]
        else:
            travel_data["list_expenses"] = [expense_data] if expense_data else []
            travel_data["total_expense"] = expense_data["amount"] if expense_data else 0.0
            list_travels.append(travel_data)

    return list_travels


def get_travel_by_id(travel_id: int):
    travel_expenses = (
        db.session.query(Travel, Expense)
        .outerjoin(Expense, Travel.id_travel == Expense.id_travel)
        .filter(Travel.id_travel == travel_id)
        .all()
    )

    travel = None
    expenses = []

    for travel_object, expense_object in travel_expenses:
        if not travel:
            travel = TravelSchema().dump(travel_object)

        if expense_object:
            expense = ExpenseSchema().dump(expense_object)
            expenses.append(expense)

    travel["list_expenses"] = expenses if expenses else None

    return travel


def update(travel_data, travel_id):
    data = TravelPutSchema().load(travel_data)
    db.session.query(Travel).filter_by(id_travel=travel_id).update(data)
    db.session.commit()
    return get_travel_by_id(travel_id)


def delete(travel_id: int):
    try:
        db.session.query(Travel).filter_by(id_travel=travel_id).delete()
        db.session.commit()
    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"TravelDBService - delete : {error}")
        raise
