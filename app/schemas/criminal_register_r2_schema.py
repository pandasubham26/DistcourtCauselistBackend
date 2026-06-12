from marshmallow import Schema, fields, validate


class CriminalRegisterRTwoSchema(Schema):
    id = fields.Int(dump_only=True)

    court_name = fields.Str(required=True, validate=validate.Length(max=255))
    case_no = fields.Str(required=True, validate=validate.Length(max=100))

    auth_estcode = fields.Str(required=True, validate=validate.Length(max=20))
    auth_judge = fields.Str(required=True, validate=validate.Length(max=255))

    serial_no = fields.Int(required=True)
    police_station = fields.Str(required=True, validate=validate.Length(max=255))
    receipt_date = fields.Date(required=True)

    crime_information = fields.Str(required=True)
    party_names = fields.Str(required=True)
    police_investigation_return = fields.Str(required=True)

    preliminary_order = fields.Str(required=False)
    final_order = fields.Str(required=False)
    remarks = fields.Str(allow_none=True)

    created_at = fields.DateTime(dump_only=True)


criminal_register_r_two_schema = CriminalRegisterRTwoSchema()

criminal_register_r_two_list_schema = CriminalRegisterRTwoSchema(many=True)