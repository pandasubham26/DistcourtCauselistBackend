from marshmallow import Schema, fields, validate


class RegisterRThirtyFourSchema(Schema):
    id = fields.Int(dump_only=True)

    serial_no = fields.Str(required=True)

    transferred = fields.Str()
    order_ix = fields.Str()
    otherwise = fields.Str()

    without_days = fields.Int()
    ex_parte = fields.Str()
    award = fields.Str()
    dismissal = fields.Str()
    admission_days = fields.Int()
    compromise = fields.Str()
    compromise_days = fields.Int()

    plaintiff = fields.Str()
    defendant = fields.Str()
    trial_days = fields.Int()
    arbitration = fields.Str()
    total_days = fields.Int()

    remarks = fields.Str()

    created_at = fields.DateTime(dump_only=True)


# Single object schema
register_r_thirty_four_schema = RegisterRThirtyFourSchema()

# Multiple object schema
register_r_thirty_fours_schema = RegisterRThirtyFourSchema(many=True)