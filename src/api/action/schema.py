from marshmallow import Schema, fields


class ActionSchema(Schema):
    id_action= fields.Integer()
    name = fields.String()
    description = fields.String()
