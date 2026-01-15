from marshmallow import Schema, fields, validate


class ExpenseSchema(Schema):
    id_expense = fields.Integer()
    name = fields.String()
    comment = fields.String()
    amount = fields.Decimal(as_string=True, validate=validate.Range(min=0))


class ExpenseTravelSchema(Schema):
    name = fields.String()
    comment = fields.String()
    amount = fields.Decimal(as_string=True, validate=validate.Range(min=0))
    id_travel = fields.Integer()


class ExpensePostSchema(Schema):
    name = fields.String()
    comment = fields.String()
    amount = fields.Decimal(as_string=True, validate=validate.Range(min=0))
