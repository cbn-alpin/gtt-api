from marshmallow import Schema, fields

from src.api.user.schema import UserSchema

class TravelSchema(Schema):
    id_travel = fields.Integer(required=False)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=False)
    start_place = fields.String(required=True)
    return_place = fields.String(required=True)
    status = fields.String(required=False)
    purpose = fields.String(required=True)
    start_municipality = fields.String(required=True)
    end_municipality = fields.String(required=True)
    destination = fields.String(required=True)
    night_count = fields.Integer(required=False)
    meal_count = fields.Integer(required=False)
    comment = fields.String(required=False)
    license_vehicle = fields.String(required=False)
    comment_vehicle = fields.String(required=False)
    start_km = fields.Integer(required=False)
    end_km = fields.Integer(required=False)
    id_user = fields.Integer(required=False)

class TravelPutSchema(Schema):
    id_travel = fields.Integer(required=False)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=False)
    start_place = fields.String(required=True)
    return_place = fields.String(required=True)
    status = fields.String(required=False)
    purpose = fields.String(required=True)
    start_municipality = fields.String(required=True)
    end_municipality = fields.String(required=True)
    destination = fields.String(required=True)
    night_count = fields.Integer(required=False)
    meal_count = fields.Integer(required=False)
    comment = fields.String(required=False)
    license_vehicle = fields.String(required=False)
    comment_vehicle = fields.String(required=False)
    start_km = fields.Integer(required=False)
    end_km = fields.Integer(required=False)



