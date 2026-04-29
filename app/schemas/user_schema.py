from ..extensions import ma
from marshmallow import fields, validate

ALLOWED_ROLES = ['app_admin', 'dist_admin', 'judge', 'user', 'advocate']


class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=6)
    )
    judge = fields.Str(required=False, allow_none=True)
    role = fields.Str(required=True, validate=validate.OneOf(ALLOWED_ROLES))
    isactive = fields.Bool()
    created_at = fields.DateTime(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)