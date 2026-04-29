from .state_schema import StateSchema
from ..extensions import ma
from marshmallow import fields, validate


ALLOWED_DISPLAY_FLAGS = ['Y', 'N']


class DistrictSchema(ma.Schema):
    state = ma.Nested(StateSchema)
    dist_code = fields.Int(dump_only=True)
    state_id = fields.Int(required=True)
    dist_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    display = fields.Str(
        required=False
    )
    create_modify = fields.DateTime(dump_only=True)


district_schema = DistrictSchema()
districts_schema = DistrictSchema(many=True)
