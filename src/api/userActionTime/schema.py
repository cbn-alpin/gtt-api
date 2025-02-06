from marshmallow import Schema, fields


class TimeSchema(Schema):
    date = fields.Date(required=True)
    duration = fields.Integer(required=True)


class ActionTimeSchema(Schema):
    id_action= fields.Integer(required=True)
    date = fields.Date(required=True)
    duration = fields.Integer(required=True)


class ActionWithTimeSchema(Schema):
    id_action= fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String()
    list_time = fields.Nested(TimeSchema)

class ProjectTimeSchema(Schema):
    id_project= fields.Integer(required=False)
    code = fields.String()
    name = fields.String()
    description = fields.String()
    start_date = fields.Date(required=False)
    end_date = fields.Date(required=False)
    is_archived = fields.Boolean()
    list_action =  fields.Nested(ActionWithTimeSchema)
