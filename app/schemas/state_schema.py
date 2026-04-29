from ..extensions import ma
from marshmallow import fields, validate


ALLOWED_DISPLAY_FLAGS = ['Y', 'N']


class StateSchema(ma.Schema):
    state_id = fields.Int(dump_only=True)
    state = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    display = fields.Str(
        required=False
    )
    create_modify = fields.DateTime(dump_only=True)


state_schema = StateSchema()
states_schema = StateSchema(many=True)
