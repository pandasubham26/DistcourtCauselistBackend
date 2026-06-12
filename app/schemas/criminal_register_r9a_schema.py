from marshmallow import Schema, fields, validate


class CriminalRegisterR9ASchema(Schema):
    id = fields.Int(dump_only=True)

    auth_estcode = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=20)
    )

    auth_judge = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200)
    )

    court_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    serial_no = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    case_no = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=90000)
    )

    person_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    nature_of_process = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    issue_date = fields.Date(required=True)

    returnable_date = fields.Date(required=True)

    receiver_date = fields.Date(required=True)

    return_date = fields.Date(
        required=False,
        allow_none=True
    )

    remarks = fields.Str(
        required=False,
        allow_none=True
    )

    created_at = fields.DateTime(dump_only=True)


criminal_register_r9a_schema = CriminalRegisterR9ASchema()

criminal_register_r9a_list_schema = CriminalRegisterR9ASchema(
    many=True
)