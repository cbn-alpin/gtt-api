from marshmallow import Schema, fields


class AuthInputSchema(Schema):
    login = fields.String(required=True)
    password = fields.String(required=True)


class UserAuthSchema(Schema):
    id_user = fields.Integer(required=True)
    email = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    is_admin = fields.Boolean()
    access_token = fields.String()
    refresh_token = fields.String()
