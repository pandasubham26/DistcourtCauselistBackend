from ..extensions import ma
from marshmallow import fields, validate


ALLOWED_DISPLAY_FLAGS = ['Y', 'N']


class TalukaSchema(ma.Schema):
    taluka_code = fields.Int(dump_only=True)
    dist_code = fields.Int(required=True)
    state_id = fields.Int(required=True)
    taluka_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    display = fields.Str(
        required=False
    )
    create_modify = fields.DateTime(dump_only=True)


taluka_schema = TalukaSchema()
talukas_schema = TalukaSchema(many=True)
