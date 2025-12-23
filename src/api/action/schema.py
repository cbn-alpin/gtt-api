from marshmallow import Schema, fields


class ActionSchema(Schema):
    id_action = fields.Integer()
    numero_action = fields.String()
    name = fields.String()
    description = fields.String()
