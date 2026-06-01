from marshmallow import Schema, fields, validate


class CriminalRegisterRThirteenSchema(Schema):
    id = fields.Int(dump_only=True)
    est_code = fields.Str(dump_only=True)

    court_name = fields.Str(required=True)
    primary_case_no = fields.Str(required=True, validate=validate.Length(max=100))
    magistrate_name = fields.Str(allow_none=True)
    trial_case_no_year = fields.Str(allow_none=True)

    complainant_name = fields.Str(allow_none=True)
    accused_name = fields.Str(allow_none=True)

    final_order_details = fields.Str(allow_none=True)
    appeal_revision_result = fields.Str(allow_none=True)

    file_class = fields.Str(allow_none=True)
    disposed_shelved_date = fields.Date(allow_none=True)
    shelf_rack_no = fields.Str(allow_none=True)
    destruction_date = fields.Date(allow_none=True)

    remarks = fields.Str(allow_none=True)


criminal_register_r13_schema = CriminalRegisterRThirteenSchema()
criminal_register_r13_many_schema = CriminalRegisterRThirteenSchema(many=True)