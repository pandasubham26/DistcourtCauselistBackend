from .designation_schema import DesignationSchema
from ..extensions import ma
from marshmallow import fields, validate


ALLOWED_DISPLAY_FLAGS = ['Y', 'N']


class JudgeSchema(ma.Schema):
    designation = ma.Nested(DesignationSchema)
    judge_code = fields.Int(dump_only=True)
    desg_code = fields.Int(required=True)
    judge_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    display = fields.Str(required=False)
    jto_dt = fields.Date(required=False)
    jfrom_dt = fields.Date(required=False)
    jocode = fields.Str(required=True)
    create_modify = fields.DateTime(dump_only=True)


judge_schema = JudgeSchema()
judges_schema = JudgeSchema(many=True)
