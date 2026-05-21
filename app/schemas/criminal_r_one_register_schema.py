from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class CriminalRegisterROneSchema(Schema):

    id = fields.Int(dump_only=True)

    court_name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=255)
        ],
        error_messages={
            "required": "Court name is required"
        }
    )

    estcode = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=10)
        ],
        error_messages={
            "required": "Establishment code is required"
        }
    )

    judge = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100)
        ],
        error_messages={
            "required": "Judge name is required"
        }
    )

    serial_no = fields.Int(
        required=True,
        validate=[
            validate.Range(min=1)
        ],
        error_messages={
            "required": "Serial number is required",
            "invalid": "Serial number must be numeric"
        }
    )

    case_no = fields.Int(
        required=True,
        validate=[
            validate.Range(min=1)
        ],
        error_messages={
            "required": "Case number is required",
            "invalid": "Case number must be numeric"
        }
    )

    case_year = fields.Int(
        required=True,
        validate=[
            validate.Range(min=1)
        ],
        error_messages={
            "required": "Case year is required",
            "invalid": "Case year must be numeric"
        }
    )

    complaint_date = fields.Date(
        required=True,
        format="%Y-%m-%d",
        error_messages={
            "required": "Complaint date is required",
            "invalid": "Invalid date format. Use YYYY-MM-DD"
        }
    )

    complainant_name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=100)
        ],
        error_messages={
            "required": "Complainant name is required"
        }
    )

    accused_names = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=255)
        ],
        error_messages={
            "required": "Accused names are required"
        }
    )

    nature_section = fields.Str(
        allow_none=True
    )

    preliminary_order = fields.Str(
        allow_none=True
    )

    final_order = fields.Str(
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

        complaint_date = data.get("complaint_date")

        if complaint_date and complaint_date > fields.Date()._deserialize(
                datetime.today().strftime("%Y-%m-%d"),
                "complaint_date",
                {}
        ):
            raise ValidationError(
                {
                    "complaint_date": [
                        "Complaint date cannot be in the future"
                    ]
                }
            )


criminal_register_r_one_schema = CriminalRegisterROneSchema()

criminal_register_r_one_list_schema = CriminalRegisterROneSchema(many=True)