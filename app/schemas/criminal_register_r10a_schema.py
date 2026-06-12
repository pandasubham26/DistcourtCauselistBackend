from marshmallow import Schema, fields, validate


class CriminalRegisterR10ASchema(Schema):
    id = fields.Int(dump_only=True)

    auth_estcode = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    auth_judge = fields.Str(required=True, validate=validate.Length(min=1, max=200))

    court_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    serial_no = fields.Int(required=True, validate=validate.Range(min=1))
    case_no = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    trail_date = fields.Date(required=True)
    prosecution_witnesses = fields.Str(required=True)
    issue_date = fields.Date(required=True)
    mode_of_service = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    return_date = fields.Date(required=True)
    suf_insuff = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    step_taken = fields.Str(required=False)

    remarks = fields.Str(required=False, allow_none=True)

    created_at = fields.DateTime(dump_only=True)


criminal_register_r10a_schema = CriminalRegisterR10ASchema()
criminal_register_r10a_list_schema = CriminalRegisterR10ASchema(many=True)