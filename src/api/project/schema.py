from marshmallow import Schema, fields

from src.api.action.schema import ActionSchema


class ProjectSchema(Schema):
    id_project= fields.Integer()
    code = fields.Integer()
    name = fields.Str()
    description = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    is_archived = fields.Bool()
    list_action =  fields.Nested(ActionSchema)
