from marshmallow import Schema, fields

from src.api.action.schema import ActionSchema


class ProjectSchema(Schema):
    id_project = fields.Integer(required=False)
    code = fields.String()
    name = fields.String()
    description = fields.String()
    start_date = fields.Date(format="%d/%m/%Y", required=False)
    end_date = fields.Date(format="%d/%m/%Y", required=False)
    is_archived = fields.Boolean()
    list_action = fields.Nested(ActionSchema)


class ProjectUpdateSchema(Schema):
    id_project = fields.Integer(required=False)
    code = fields.String(required=False)
    name = fields.String(required=False)
    description = fields.String(allow_none=True, required=False)
    start_date = fields.Date(format="%d/%m/%Y", required=False)
    end_date = fields.Date(format="%d/%m/%Y", required=False)
    is_archived = fields.Boolean(required=False)


class ProjectInputSchema(Schema):
    code = fields.Integer(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    start_date = fields.Date(format="%d/%m/%Y", required=True)
    end_date = fields.Date(format="%d/%m/%Y", required=False)
    is_archived = fields.Bool(required=False)
