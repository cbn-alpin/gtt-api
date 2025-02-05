from marshmallow import Schema, fields

from src.api.action.schema import ActionSchema


class ProjectSchema(Schema):
    id_project= fields.Integer(required=False)
    code = fields.Integer()
    name = fields.String()
    description = fields.String()
    start_date = fields.Date(required=False)
    end_date = fields.Date(required=False)
    is_archived = fields.Boolean()
    list_action =  fields.Nested(ActionSchema)


class ProjectUpdateSchema(Schema):
    id_project= fields.Integer(required=False)
    code = fields.Integer()
    name = fields.String()
    description = fields.String()
    start_date = fields.Date()
    end_date = fields.Date()
    is_archived = fields.Boolean()

class ProjectInputSchema(Schema):
    code = fields.Integer(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=False)
    is_archived = fields.Bool(required=False)
