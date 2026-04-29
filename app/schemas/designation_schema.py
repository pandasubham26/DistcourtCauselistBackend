from ..extensions import ma
from marshmallow import fields, validate


ALLOWED_DISPLAY_FLAGS = ['Y', 'N']


class DesignationSchema(ma.Schema):
    desgcode = fields.Int(dump_only=True)
    desgname = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    display = fields.Str(
        required=False
    )
    create_modify = fields.DateTime(dump_only=True)


designation_schema = DesignationSchema()
designations_schema = DesignationSchema(many=True)
