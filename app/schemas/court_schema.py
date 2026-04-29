from ..extensions import ma
from marshmallow import fields, validate


class CourtNameSchema(ma.Schema):
    est_code = fields.Str(required=True, validate=validate.Length(max=6))
    court_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    state = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    district = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    create_modify = fields.DateTime(dump_only=True)


court_schema = CourtNameSchema()
courts_schema = CourtNameSchema(many=True)
