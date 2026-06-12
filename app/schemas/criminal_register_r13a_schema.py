from marshmallow import Schema, fields, validate


class CriminalRegisterR13ASchema(Schema):
    id = fields.Int(dump_only=True)

    auth_estcode = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    auth_judge = fields.Str(required=True, validate=validate.Length(min=1, max=200))

    court_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    serial_no = fields.Int(required=True, validate=validate.Range(min=1))
    case_no = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    parties_name = fields.Str(required=True)
    dormant_order_date = fields.Date(required=True)
    record_room_received_date = fields.Date(required=True)
    shelf_rack_no = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    requisition_received_date = fields.Date(required=False, allow_none=True)
    trial_court_sent_date = fields.Date(required=False, allow_none=True)

    remarks = fields.Str(required=False, allow_none=True)

    created_at = fields.DateTime(dump_only=True)


criminal_register_r13a_schema = CriminalRegisterR13ASchema()
criminal_register_r13a_list_schema = CriminalRegisterR13ASchema(many=True)