from ..extensions import ma
from marshmallow import fields, validate


class CaseFileUploadSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    bulk_no = fields.Str(dump_only=True)  # auto-generated
    barcode = fields.Str(required=True)
    cino = fields.Str(required=False, allow_none=True)
    court = fields.Str(required=True)
    judge = fields.Str(required=True)
    est_code = fields.Str(required=True)

    cis_case_type = fields.Str(required=True)
    cis_case_no = fields.Int(required=True)
    cis_case_year = fields.Int(required=True)

    reg_case_type = fields.Str(required=True)
    reg_case_no = fields.Int(required=True)
    reg_case_year = fields.Int(required=True)

    pet_name = fields.Str(required=False, allow_none=True)
    pet_adv = fields.Str(required=False, allow_none=True)
    res_name = fields.Str(required=False, allow_none=True)
    res_adv = fields.Str(required=False, allow_none=True)

    status = fields.Str(dump_only=True)
    display = fields.Str(dump_only=True)

    uploaded_by = fields.Str(required=False, allow_none=True)
    uploaded_at = fields.DateTime(dump_only=True)


casefile_upload_schema = CaseFileUploadSchema()
casefile_uploads_schema = CaseFileUploadSchema(many=True)