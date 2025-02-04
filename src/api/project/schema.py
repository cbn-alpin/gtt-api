from dataclasses import fields
from marshmallow import Schema

from ..action import ActionSchema


class ProjectSchema(Schema):
    id_project= fields.Integer()
    code = fields.Integer()
    name = fields.Str()
    description = fields.Text()
    start_date = fields.Date()
    end_date = fields.Date()
    is_archived = fields.Bool()
    list_action =  fields.Nested(ActionSchema) 