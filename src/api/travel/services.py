from flask import current_app
import sqlalchemy
from src.api import db
from src.api.expense.schema import ExpenseSchema
from src.api.travel.schema import TravelSchema
from src.models import Expense, Travel
from src.api.exception import DBInsertException

def create_travel(user_id, project_id, travel_data: dict) -> int:
    try:
        schema = TravelSchema()
        travel = schema.load(travel_data)
        
        new_travel = Travel(
            status=travel['status'],
            start_date=travel.get('start_date'),
            end_date=travel.get('end_date'),
            start_place=travel.get('start_place'),
            return_place=travel.get('return_place'),
            purpose=travel.get('purpose'),
            start_municipality=travel.get('start_municipality'),
            end_municipality=travel.get('end_municipality'),
            destination=travel.get('destination'),
            night_count=travel.get('night_count'),
            meal_count=travel.get('meal_count'),
            comment=travel.get('comment'),
            license_vehicle=travel.get('license_vehicle'),
            comment_vehicle=travel.get('comment_vehicle'),
            start_km=travel.get('start_km'),
            end_km=travel.get('end_km'),
            id_user=user_id,
            id_project=project_id
        )

        db.session.add(new_travel)
        db.session.commit()
        return new_travel.id_travel

    except ValueError as error:
        db.session.rollback()
        current_app.logger.error(f"travelDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()

    except sqlalchemy.exc.IntegrityError as error:
        db.session.rollback()
        current_app.logger.error(f"travelDBService - insert : {error}")
        if db.session is not None:
            db.session.close()
        raise DBInsertException()



def get_travels(user_id):
    travels_expenses_tuple = (
        db.session.query(Travel, Expense)
        .outerjoin(Expense, Travel.id_travel == Expense.id_travel)
        .filter(Travel.id_user == user_id)
        .all()
    )

    list_travels = []
    for travel, expense in travels_expenses_tuple:
        travel_data = TravelSchema().dump(travel)
        expense_data = ExpenseSchema().dump(expense) if expense else None

        existing_travel = next((t for t in list_travels if t["id_travel"] == travel_data["id_travel"]), None)

        if existing_travel:
            if expense_data:
                existing_travel["list_expenses"].append(expense_data)
                existing_travel["total_expense"] += expense_data["amount"]
        else:
            travel_data["list_expenses"] = [expense_data] if expense_data else []
            travel_data["total_expense"] = expense_data["amount"] if expense_data else 0.0
            list_travels.append(travel_data)

    db.session.close()
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

    db.session.close()
    return travel


def update(travel_data, travel_id):
    data = TravelPutSchema().load(travel_data)
    db.session.query(Travel).filter_by(id_travel=travel_id).update(data)
    db.session.commit()
    db.session.close()
    return get_travel_by_id(travel_id)