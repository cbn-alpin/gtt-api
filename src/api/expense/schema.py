from marshmallow import Schema, fields


class ExpenseSchema(Schema):
    id_expense = fields.Integer()
    name = fields.String()
    comment = fields.String()
    amount = fields.Number()


class ExpenseTravelSchema(Schema):
    name = fields.String()
    comment = fields.String()
    amount = fields.Number()
    id_travel = fields.Integer()


class ExpensePostSchema(Schema):
    name = fields.String()
    comment = fields.String()
    amount = fields.Number()
