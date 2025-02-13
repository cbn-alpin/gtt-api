from marshmallow import Schema, fields


class ExpenseSchema(Schema):
    id_expense= fields.Integer()
    name = fields.String()
    comment = fields.String()
    description = fields.String()
    amount= fields.Number()