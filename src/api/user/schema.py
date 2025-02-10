
from marshmallow import Schema, fields


class UserSchema(Schema):
    id_user= fields.Integer(required=True)
    email = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    is_admin = fields.Boolean()
