from marshmallow import fields, validate
from ..extensions import ma


class RegisterRTwentySchema(ma.Schema):
    id = fields.Integer(dump_only=True)

    court_name = fields.String(required=True, validate=validate.Length(max=255))
    consecutive_no = fields.Integer(required=True)

    case_number = fields.Integer(required=True)  # changed to string
    parties = fields.String(required=True)

    decision_date = fields.Date(allow_none=True)
    file_details = fields.String(allow_none=True)

    disposed_date = fields.Date(allow_none=True)
    shelf_details = fields.String(allow_none=True)

    remarks = fields.String(allow_none=True)

    created_at = fields.DateTime(dump_only=True)


# Single object schema
register_r_twenty_schema = RegisterRTwentySchema()

# Multiple object schema
register_r_twentys_schema = RegisterRTwentySchema(many=True)