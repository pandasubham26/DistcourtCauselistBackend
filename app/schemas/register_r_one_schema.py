from ..extensions import ma
from marshmallow import fields, validate, validates_schema, ValidationError


class RegisterROneSchema(ma.Schema):
    id = fields.Integer(dump_only=True)

    # -------------------------
    # Court Information
    # -------------------------
    court_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=255)
    )

    location = fields.String(
        required=True,
        validate=validate.Length(min=2, max=255)
    )

    year = fields.Integer(required=True)

    # -------------------------
    # Suit Details
    # -------------------------
    presentation_date = fields.Date(required=True)

    serial_no = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    suit_name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=255)
    )

    casetype = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    # -------------------------
    # Plaintiff Details
    # -------------------------
    plaintiff_name = fields.String(required=True)
    plaintiff_description = fields.String(allow_none=True)
    plaintiff_address = fields.String(allow_none=True)

    # -------------------------
    # Defendant Details
    # -------------------------
    defendant_name = fields.String(required=True)
    defendant_description = fields.String(allow_none=True)
    defendant_address = fields.String(allow_none=True)

    # -------------------------
    # Claim Details
    # -------------------------
    claim_value = fields.String(allow_none=True)
    cause_of_action = fields.String(allow_none=True)
    remarks = fields.String(allow_none=True)

    # -------------------------
    # Judgment Details
    # -------------------------
    judgement_from_whom = fields.String(allow_none=True)
    judgement_amount = fields.String(allow_none=True)
    judgement_date = fields.Date(allow_none=True)
    judgement_for_what = fields.String(allow_none=True)

    # -------------------------
    # Appeal Details
    # -------------------------
    appeal_date = fields.Date(allow_none=True)
    appeal_against = fields.String(allow_none=True)
    appeal_amount = fields.String(allow_none=True)
    appeal_number_year = fields.String(allow_none=True)
    appeal_order_details = fields.String(allow_none=True)

    # -------------------------
    # Adjustment Details
    # -------------------------
    adjustment_court = fields.String(allow_none=True)
    adjustment_name = fields.String(allow_none=True)
    adjustment_particulars = fields.String(allow_none=True)

    # -------------------------
    # Execution Details
    # -------------------------
    execution_date = fields.Date(allow_none=True)
    serial_no_under_rule = fields.String(allow_none=True)
    execution_application_details = fields.String(allow_none=True)
    execution_against_whom = fields.String(allow_none=True)
    execution_for_what = fields.String(allow_none=True)

    # -------------------------
    # Financial Details
    # -------------------------
    costs_amount = fields.String(allow_none=True)
    paid_into_court = fields.String(allow_none=True)
    relief_amount_due = fields.String(allow_none=True)

    # -------------------------
    # Additional Details
    # -------------------------
    person_detained = fields.String(allow_none=True)
    return_minute = fields.String(allow_none=True)
    appeal_revision_orders = fields.String(allow_none=True)

    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_year(self, data, **kwargs):
        year = data.get("year")

        if year and (year < 1900 or year > 2100):
            raise ValidationError(
                "Year must be between 1900 and 2100",
                field_name="year"
            )


# Single object schema
register_r_one_schema = RegisterROneSchema()

# Multiple object schema
register_r_ones_schema = RegisterROneSchema(many=True)