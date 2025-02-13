from flask import current_app
import sqlalchemy
from src.api import db
from src.api.travel.schema import TravelSchema
from src.models import Travel
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

def get_travel_by_id(travel_id : int):
    travel_object = db.session.query(Travel).filter(Travel.id_travel== travel_id).first()
    schema = TravelSchema()
    action= schema.dump(travel_object)
    db.session.close()
    return action

def update(travel_data, travel_id):
    data = TravelSchema().load(travel_data)
    db.session.query(Travel).filter_by(id_travel=travel_id).update(data)
    db.session.commit()
    db.session.close()
    return get_travel_by_id(travel_id)