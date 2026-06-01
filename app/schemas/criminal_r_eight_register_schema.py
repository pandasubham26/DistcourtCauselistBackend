from marshmallow import Schema, fields, validate


class RegisterREightSchema(Schema):
    id = fields.Int(dump_only=True)
    serial_no = fields.Int(required=False)
    witness_name = fields.Str(required=False, validate=validate.Length(max=255))
    case_number = fields.Str(required=False, validate=validate.Length(max=100))
    est_code = fields.Str(required=False, validate=validate.Length(max=10))
    judge = fields.Str(required=False, validate=validate.Length(max=100))
    attendance_day_1 = fields.Date(allow_none=True)
    attendance_day_2 = fields.Date(allow_none=True)
    attendance_day_3 = fields.Date(allow_none=True)
    attendance_day_4 = fields.Date(allow_none=True)
    attendance_day_5 = fields.Date(allow_none=True)
    attendance_day_6 = fields.Date(allow_none=True)
    discharged_day_1 = fields.Date(allow_none=True)
    discharged_day_2 = fields.Date(allow_none=True)
    discharged_day_3 = fields.Date(allow_none=True)
    discharged_after_day_3 = fields.Date(allow_none=True)
    examined = fields.Str(allow_none=True, validate=validate.Length(max=50))
    cross_examination_declined = fields.Str(allow_none=True, validate=validate.Length(max=50))
    not_examined = fields.Str(allow_none=True, validate=validate.Length(max=50))
    presiding_officer_initial = fields.Str(allow_none=False, validate=validate.Length(max=100))
    remarks = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


register_r8_schema = RegisterREightSchema()
register_r8_many_schema = RegisterREightSchema(many=True)