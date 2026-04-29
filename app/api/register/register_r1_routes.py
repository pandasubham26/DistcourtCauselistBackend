from app.schemas.register_r_one_schema import register_r_one_schema
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from sqlalchemy import asc, desc, or_, and_, func
from app.extensions import db
from app.models.register.register_r1_model import RegisterROne
from app.utils import success_response, error_response, require_group, log_action

register_r1_bp = Blueprint(
    "register_r1_bp",
    __name__,
    url_prefix="/register/r1"
)


def parse_date(date_value):
    if not date_value:
        return None
    try:
        return datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        return None


@register_r1_bp.route("/create", methods=["POST"])
@jwt_required()
@require_group(min_group="readandwrite")
def create_register_r1(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return error_response(
                error="validation_error",
                message="Request payload is required",
                status=400
            )

        # Required field validation
        required_fields = [
            "court_name",
            "location",
            "year",
            "presentation_date",
            "serial_no",
            "suit_name",
            "casetype",
            "plaintiff_name",
            "defendant_name"
        ]

        missing_fields = [
            field for field in required_fields
            if not data.get(field)
        ]

        if missing_fields:
            return error_response(
                error="validation_error",
                message="Required fields are missing",
                details={
                    "missing_fields": missing_fields
                },
                status=400
            )

        register_entry = RegisterROne(
            court_name=data.get("court_name"),
            location=data.get("location"),
            year=data.get("year"),

            presentation_date=parse_date(
                data.get("presentation_date")
            ),
            serial_no=data.get("serial_no"),
            suit_name=data.get("suit_name"),
            casetype=data.get("casetype"),

            plaintiff_name=data.get("plaintiff_name"),
            plaintiff_description=data.get("plaintiff_description"),
            plaintiff_address=data.get("plaintiff_address"),

            defendant_name=data.get("defendant_name"),
            defendant_description=data.get("defendant_description"),
            defendant_address=data.get("defendant_address"),

            claim_value=data.get("claim_value"),
            cause_of_action=data.get("cause_of_action"),
            remarks=data.get("remarks"),

            judgement_from_whom=data.get("judgement_from_whom"),
            judgement_amount=data.get("judgement_amount"),
            judgement_date=parse_date(
                data.get("judgement_date")
            ),

            appeal_date=parse_date(
                data.get("appeal_date")
            ),
            appeal_against=data.get("appeal_against"),
            appeal_amount=data.get("appeal_amount"),

            adjustment_court=data.get("adjustment_court"),
            adjustment_name=data.get("adjustment_name"),
            execution_date=parse_date(
                data.get("execution_date")
            ),
            judgement_for_what=data.get("judgement_for_what"),

            appeal_number_year=data.get("appeal_number_year"),
            appeal_order_details=data.get("appeal_order_details"),

            adjustment_particulars=data.get("adjustment_particulars"),

            serial_no_under_rule=data.get("serial_no_under_rule"),
            execution_application_details=data.get("execution_application_details"),
            execution_against_whom=data.get("execution_against_whom"),
            execution_for_what=data.get("execution_for_what"),

            costs_amount=data.get("costs_amount"),
            paid_into_court=data.get("paid_into_court"),
            person_detained=data.get("person_detained"),
            return_minute=data.get("return_minute"),
            appeal_revision_orders=data.get("appeal_revision_orders"),
            relief_amount_due=data.get("relief_amount_due")
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R1",
            entity="register_r1",
            entity_id=register_entry.id,
            details={
                "serial_no": register_entry.serial_no,
                "suit_name": register_entry.suit_name,
                "court_name": register_entry.court_name
            }
        )

        return success_response(
            data=register_entry.to_dict(),
            message="Register R1 entry created successfully",
            status=200
        )

    except Exception as e:
        db.session.rollback()

        return error_response(
            error="server_error",
            message="Failed to create Register R1 entry",
            details=str(e),
            status=500
        )
    

@register_r1_bp.route("/getroneregisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r1_list(estcode):

    try:
        # Handle preflight request
        if request.method == "OPTIONS":
            return "", 200

        # Validate establishment code
        jwt_estcode = get_jwt().get("estcode")
        if jwt_estcode != estcode:
            return error_response(
                error="forbidden",
                message="Invalid establishment code",
                status=403
            )

        # Query params
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)
        status = request.args.get("status", default="", type=str)
        search = request.args.get("search", default="", type=str)
        sort_by = request.args.get("sortBy", default="created_at", type=str)
        order = request.args.get("order", default="desc", type=str)
        casetype = request.args.get("casetype", default="", type=str)

        if page < 1 or limit < 1:
            return error_response(
                error="validation_error",
                message="Page and limit must be greater than 0",
                status=400
            )

        # Sorting
        sort_columns = {
            "casetype": RegisterROne.casetype,
            "created_at": RegisterROne.created_at,
            "serial_no": RegisterROne.serial_no,
            "court_name": RegisterROne.court_name
        }

        sort_column = sort_columns.get(
            sort_by,
            RegisterROne.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            RegisterROne.casetype,
            RegisterROne.court_name,
            func.count(RegisterROne.id).label("count")
        )

        # Case type filter
        if casetype and casetype.lower() != "all":
            query = query.filter(
                RegisterROne.casetype.ilike(f"%{casetype}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    RegisterROne.serial_no.ilike(f"%{search}%"),
                    RegisterROne.suit_name.ilike(f"%{search}%"),
                    RegisterROne.plaintiff_name.ilike(f"%{search}%"),
                    RegisterROne.defendant_name.ilike(f"%{search}%"),
                    RegisterROne.court_name.ilike(f"%{search}%")
                )
            )

        query = query.group_by(RegisterROne.casetype, RegisterROne.court_name)

        total = query.count()

        register_entries = (
            query
            .order_by(order_func(sort_column))
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        response_data = [
            {
                "court_name": row.court_name,
                "casetype": row.casetype,
                "count": row.count
            }
            for row in register_entries
        ]

        # casefile_list = register_r_one_schema.dump(register_entries, many=True)

        response_data = {
            "registers": response_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            },
            "filters": {
                "search": search,
                "status": status,
                "casetype": casetype,
                "sortBy": sort_by,
                "order": order
            }
        }

        return success_response(
            data=response_data,
            message="Register R1 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R1 entries:" + str(e),
            details=str(e),
            status=500
        )
    

@register_r1_bp.route("/getroneregisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r1_list_by_court(estcode):
    
    try:
        # Handle preflight request
        if request.method == "OPTIONS":
            return "", 200

        # Validate establishment code
        jwt_estcode = get_jwt().get("estcode")
        if jwt_estcode != estcode:
            return error_response(
                error="forbidden",
                message="Invalid establishment code",
                status=403
            )

        court_name = request.args.get("court_name", default="", type=str)
        case_type = request.args.get("casetype", default="", type=str)

        if not court_name:
            return error_response(
                error="validation_error",
                message="court_name query parameter is required",
                status=400
            )
        
        if court_name:
            query = RegisterROne.query.filter(RegisterROne.court_name == court_name)
        
        if not case_type:
            return error_response(
                error="validation_error",
                message="casetype query parameter is required",
                status=400
            )

        if case_type:
            query = query.filter(RegisterROne.casetype == case_type)
        
        total = query.count()

        files = (
            query.order_by(desc(RegisterROne.created_at))
            .all()
        )

        casefile_list = register_r_one_schema.dump(files, many=True)

        return success_response(
            data=casefile_list,
            message="Register R1 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R1 entries:" + str(e),
            details=str(e),
            status=500
        )