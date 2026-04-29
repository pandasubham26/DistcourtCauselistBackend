from ..extensions import ma
from marshmallow import fields, validate


class CaseTypeSchema(ma.Schema):
    case_type = fields.Int(dump_only=True)
    type_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    full_form = fields.Str(required=True, validate=validate.Length(max=100))
    type_flag = fields.Str(
        required=False
    )
    display = fields.Str(
        required=False
    )
    create_modify = fields.DateTime(dump_only=True)


casetype_schema = CaseTypeSchema()
casetypes_schema = CaseTypeSchema(many=True)
