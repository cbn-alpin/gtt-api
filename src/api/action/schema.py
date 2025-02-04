from dataclasses import fields
from marshmallow import Schema


class ActionSchema(Schema):
    id_action= fields.Integer()
    name = fields.Str()
    description = fields.Text()
 