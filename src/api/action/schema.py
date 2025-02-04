from marshmallow import Schema
import marshmallow


class ActionSchema(Schema):
    id_action= marshmallow.fields.Integer()
    name = marshmallow.fields.String()
    description = marshmallow.fields.String()
