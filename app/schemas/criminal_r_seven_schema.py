from marshmallow import Schema, fields, validate


class RegisterRSevenSchema(Schema):
    id = fields.Int(dump_only=True)
    serial_no = fields.Int(required=True, validate=validate.Length(max=50))
    nature_of_documents = fields.Str(
        required=True,
        validate=validate.Length(max=255)
    )
    date = fields.Date(required=True)
    case_number = fields.Str(
        required=True,
        validate=validate.Length(max=100)
    )
    est_code = fields.Str(
        required=True,
        validate=validate.Length(max=10)
    )
    judge = fields.Str(
        required=True,
        validate=validate.Length(max=100)
    )
    court_name = fields.Str(
        required=True,
        validate=validate.Length(max=255)
    )
    process_fee_rs = fields.Int(
        required=False,
        load_default=0,
        validate=validate.Range(min=0)
    )
    process_fee_ps = fields.Int(
        required=False,
        load_default=0,
        validate=validate.Range(min=0, max=99)
    )
    affidavit_fee_rs = fields.Int(
        required=False,
        load_default=0,
        validate=validate.Range(min=0)
    )
    affidavit_fee_ps = fields.Int(
        required=False,
        load_default=0,
        validate=validate.Range(min=0, max=99)
    )
    other_fee_rs = fields.Int(
        required=False,
        load_default=0,
        validate=validate.Range(min=0)
    )
    other_fee_ps = fields.Int(
        required=False,
        load_default=0,
        validate=validate.Range(min=0, max=99)
    )
    remarks = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


register_r7_schema = RegisterRSevenSchema()
register_r7_many_schema = RegisterRSevenSchema(many=True)