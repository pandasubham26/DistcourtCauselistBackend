from datetime import datetime

from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class CriminalRegisterRThreeSchema(Schema):

    id = fields.Int(dump_only=True)

    court_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=255),
        error_messages={
            "required": "Court name is required"
        }
    )

    estcode = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=10),
        error_messages={
            "required": "Establishment code is required"
        }
    )

    judge = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={
            "required": "Judge name is required"
        }
    )

    serial_no = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "Serial number is required",
            "invalid": "Serial number must be numeric"
        }
    )

    case_no = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "Case number is required",
            "invalid": "Case number must be numeric"
        }
    )

    case_year = fields.Int(
        required=True,
        validate=validate.Range(min=1900, max=2100),
        error_messages={
            "required": "Case year is required",
            "invalid": "Case year must be numeric"
        }
    )

    date_of_institution = fields.Date(
        required=True,
        format="%Y-%m-%d",
        error_messages={
            "required": "Date of institution is required",
            "invalid": "Invalid date format. Use YYYY-MM-DD"
        }
    )

    date_of_receipt = fields.Date(
        required=True,
        format="%Y-%m-%d",
        error_messages={
            "required": "Date of receipt is required",
            "invalid": "Invalid date format. Use YYYY-MM-DD"
        }
    )

    complainant_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={
            "required": "Complainant name is required"
        }
    )

    accused_count = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            "required": "Accused count is required",
            "invalid": "Accused count must be numeric"
        }
    )

    nature_section = fields.Str(
        allow_none=True
    )

    final_order_date = fields.Str(
        allow_none=True
    )

    appeal_revision_result = fields.Str(
        allow_none=True
    )

    remarks = fields.Str(
        allow_none=True
    )

    created_at = fields.DateTime(
        dump_only=True
    )

    @validates_schema
    def validate_dates(self, data, **kwargs):

        today = datetime.today().date()

        institution_date = data.get("date_of_institution")
        receipt_date = data.get("date_of_receipt")

        if institution_date and institution_date > today:
            raise ValidationError(
                {
                    "date_of_institution": [
                        "Date of institution cannot be in the future"
                    ]
                }
            )

        if receipt_date and receipt_date > today:
            raise ValidationError(
                {
                    "date_of_receipt": [
                        "Date of receipt cannot be in the future"
                    ]
                }
            )

        if institution_date and receipt_date:

            if receipt_date < institution_date:
                raise ValidationError(
                    {
                        "date_of_receipt": [
                            "Date of receipt cannot be earlier than institution date"
                        ]
                    }
                )


criminal_register_r_three_schema = CriminalRegisterRThreeSchema()

criminal_register_r_three_list_schema = CriminalRegisterRThreeSchema(many=True)