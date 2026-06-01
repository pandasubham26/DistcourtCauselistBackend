from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from sqlalchemy import asc, desc, func, or_, and_

from app.estcode_db import get_cis_db_key
from app.extensions import db
from app.models.cis.registry import get_cis_model
from app.models.register.criminal_register_model import CriminalRegisterROne, CriminalRegisterRThree, \
    CriminalRegisterREight, CriminalRegisterRThirteen
from app.schemas.criminal_r_eight_register_schema import register_r8_schema
from app.schemas.criminal_r_one_register_schema import criminal_register_r_one_schema
from app.schemas.criminal_r_thirteen_register_schema import criminal_register_r13_schema
from app.schemas.criminal_r_three_register_schema import criminal_register_r_three_schema
from app.utils import error_response, success_response, log_action

register_r_bp = Blueprint(
    "register_r_bp",
    __name__,
    url_prefix="/register/criminal"
)

def parse_date(date_value):
    if not date_value:
        return None
    try:
        return datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        return None


@register_r_bp.route("/createcriminalroneregister", methods=["POST"])
@jwt_required()
def cri_create_register_r1(estcode):
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
            "case_no",
            "case_year",
            "auth_estcode",
            "auth_judge",
            "complaint_date",
            "serial_no",
            "complainant_name",
            "accused_names",
            "nature_section",
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

        register_entry = CriminalRegisterROne(
            court_name=data.get("court_name"),
            estcode=data.get("auth_estcode"),
            judge=data.get("auth_judge"),
            complaint_date=parse_date(
                data.get("complaint_date")
            ),
            serial_no=data.get("serial_no"),
            case_no=data.get("case_no"),
            case_year=data.get("case_year"),
            complainant_name=data.get("complainant_name"),
            accused_names=data.get("accused_names"),

            nature_section=data.get("nature_section"),
            preliminary_order=data.get("preliminary_order"),
            final_order=data.get("final_order"),
            remarks=data.get("remarks")
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R1",
            entity="criminal_register_r1",
            entity_id=register_entry.id,
            details={
                "serial_no": register_entry.serial_no,
                "estcode": register_entry.estcode,
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


@register_r_bp.route("/getroneregisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r_list(estcode):

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
        judge = request.args.get("judge", default="", type=str)

        if page < 1 or limit < 1:
            return error_response(
                error="validation_error",
                message="Page and limit must be greater than 0",
                status=400
            )

        # Sorting
        sort_columns = {
            "created_at": CriminalRegisterROne.created_at,
            "serial_no": CriminalRegisterROne.serial_no,
            "court_name": CriminalRegisterROne.court_name
        }

        sort_column = sort_columns.get(
            sort_by,
            CriminalRegisterROne.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            CriminalRegisterROne.court_name,
            func.count(CriminalRegisterROne.id).label("count")
        )

        # Case type filter
        if judge:
            query = query.filter(
                CriminalRegisterROne.judge.ilike(f"%{judge}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    CriminalRegisterROne.serial_no.ilike(f"%{search}%"),
                    CriminalRegisterROne.complainant_name.ilike(f"%{search}%"),
                    CriminalRegisterROne.accused_names.ilike(f"%{search}%"),
                    CriminalRegisterROne.nature_section.ilike(f"%{search}%"),
                    CriminalRegisterROne.court_name.ilike(f"%{search}%")
                )
            )

        query = query.group_by(CriminalRegisterROne.court_name)

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
                "judge": judge,
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


@register_r_bp.route("/getroneregisterlistbycourt", methods=["GET", "OPTIONS"])
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

        if not court_name:
            return error_response(
                error="validation_error",
                message="court_name query parameter is required",
                status=400
            )

        if court_name:
            query = CriminalRegisterROne.query.filter(CriminalRegisterROne.court_name == court_name)


        total = query.count()

        files = (
            query.order_by(desc(CriminalRegisterROne.created_at))
            .all()
        )

        casefile_list = criminal_register_r_one_schema.dump(files, many=True)

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


@register_r_bp.route("/getcasedetailsbycasenoandyear", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_case_details_by_no_yr(estcode):
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

        case_no = request.args.get('case_no')
        case_year = request.args.get('case_year')

        if not case_no:
            return error_response(
                'validation_error',
                'Case number is required',
                status=400
            )

        query = CriminalRegisterROne.query.filter(CriminalRegisterROne.case_no == case_no)
        if case_year:
            CriminalRegisterROne.query.filter(CriminalRegisterROne.case_year == case_year)

        case = query.first()

        if not case:
            return error_response(
                'not_found',
                'Case details not found',
                status=404
            )

        data = {
            "complainant_name": case.complainant_name
        }

        return success_response(
            data=data,
            message='Case details fetched successfully',
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R1 entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/createrthreeregister", methods=["POST"])
@jwt_required()
def cri_create_register_r3(estcode):
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
        print(data)

        if not data:
            return error_response(
                error="validation_error",
                message="Request payload is required",
                status=400
            )

        # Required field validation
        required_fields = [
            "court_name",
            "case_no",
            "case_year",
            "auth_estcode",
            "auth_judge",
            "serial_no",
            "complainant_name"
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

        register_entry = CriminalRegisterRThree(
            court_name=data.get("court_name"),
            estcode=data.get("auth_estcode"),
            judge=data.get("auth_judge"),
            date_of_institution=parse_date(
                data.get("date_of_institution")
            ),
            date_of_receipt=parse_date(data.get("date_of_receipt")),
            serial_no=data.get("serial_no"),
            case_no=data.get("case_no"),
            case_year=data.get("case_year"),
            complainant_name=data.get("complainant_name"),
            accused_count=data.get("accused_count"),
            nature_section=data.get("nature_section"),
            final_order_date=data.get("final_order_date"),
            appeal_revision_result=data.get("appeal_revision_result"),
            remarks=data.get("remarks")
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R3",
            entity="criminal_register_r3",
            entity_id=register_entry.id,
            details={
                "serial_no": register_entry.serial_no,
                "estcode": register_entry.estcode,
                "court_name": register_entry.court_name
            }
        )

        return success_response(
            data=register_entry.to_dict(),
            message="Register R3 entry created successfully",
            status=200
        )

    except Exception as e:
        db.session.rollback()

        return error_response(
            error="server_error",
            message="Failed to create Register R3 entry",
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrthreeregisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r3_list(estcode):

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
        judge = request.args.get("judge", default="", type=str)

        if page < 1 or limit < 1:
            return error_response(
                error="validation_error",
                message="Page and limit must be greater than 0",
                status=400
            )

        # Sorting
        sort_columns = {
            "created_at": CriminalRegisterRThree.created_at,
            "serial_no": CriminalRegisterRThree.serial_no,
            "court_name": CriminalRegisterRThree.court_name
        }

        sort_column = sort_columns.get(
            sort_by,
            CriminalRegisterRThree.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            CriminalRegisterRThree.court_name,
            func.count(CriminalRegisterRThree.id).label("count")
        )

        # Case type filter
        if judge:
            query = query.filter(
                CriminalRegisterRThree.judge.ilike(f"%{judge}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    CriminalRegisterRThree.serial_no.ilike(f"%{search}%"),
                    CriminalRegisterRThree.complainant_name.ilike(f"%{search}%"),
                    CriminalRegisterRThree.nature_section.ilike(f"%{search}%"),
                    CriminalRegisterRThree.court_name.ilike(f"%{search}%")
                )
            )

        query = query.group_by(CriminalRegisterRThree.court_name)

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
                "judge": judge,
                "sortBy": sort_by,
                "order": order
            }
        }

        return success_response(
            data=response_data,
            message="Register R3 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R3 entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrthreeregisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r3_list_by_court(estcode):
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

        if not court_name:
            return error_response(
                error="validation_error",
                message="court_name query parameter is required",
                status=400
            )

        if court_name:
            query = CriminalRegisterRThree.query.filter(CriminalRegisterROne.court_name == court_name)


        total = query.count()

        files = (
            query.order_by(desc(CriminalRegisterRThree.created_at))
            .all()
        )

        casefile_list = criminal_register_r_three_schema.dump(files, many=True)

        return success_response(
            data=casefile_list,
            message="Register R3 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R1 entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrsixregisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r6_list(estcode):

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
        judge = request.args.get("judge", default="", type=str)

        if page < 1 or limit < 1:
            return error_response(
                error="validation_error",
                message="Page and limit must be greater than 0",
                status=400
            )

        db_key = get_cis_db_key(estcode)
        Judge_Name = get_cis_model(db_key, 'judge_name_t')
        JudgeWithCourtNo = get_cis_model(db_key, 'judge_t')
        CivilT = get_cis_model(db_key, 'civil_t')
        CaseTypeT = get_cis_model(db_key, 'case_type_t')

        judge_record = (
            db.session.query(Judge_Name)
            .filter(Judge_Name.judge_name.ilike(f"%{judge}%"))
            .first()
        )

        if not judge_record:
            return error_response('judge_not_found', f"No judge found matching '{judge}'.", status=404)

        jocode = judge_record.judge_code

        judge_court_no = (
            db.session.query(JudgeWithCourtNo)
            .filter(JudgeWithCourtNo.judge_code == jocode,
                    JudgeWithCourtNo.to_dt.is_(None))
            .first()
        )

        if not judge_court_no:
            return error_response('judge_not_found', f"No  found matching '{judge}'.", status=404)

        court_no = judge_court_no.court_no

        query = (
            db.session.query(
                CaseTypeT.type_name,
                CivilT.reg_no,
                CivilT.reg_year,
                CivilT.cino
            ).select_from(CivilT)
            .join(JudgeWithCourtNo, CivilT.court_no == JudgeWithCourtNo.court_no)
            .join(CaseTypeT, CivilT.regcase_type == CaseTypeT.case_type)
            .filter(
                and_(
                    CivilT.date_of_decision.is_(None),
                    JudgeWithCourtNo.to_dt.is_(None),
                    CivilT.court_no == court_no
                )
            )
            .order_by(CivilT.regcase_type)
        )

        if search:
            query = query.filter(
                or_(
                    CaseTypeT.type_name.ilike(f"%{search}%"),
                    func.cast(CivilT.reg_no, db.String).ilike(f"%{search}%"),
                    func.cast(CivilT.reg_year, db.String).ilike(f"%{search}%")
                )
            )

        query = query.group_by(
            CaseTypeT.type_name,
            CivilT.regcase_type,
            CivilT.reg_no,
            CivilT.reg_year,
            CivilT.cino
        )

        sort_columns = {
            "case_type": CaseTypeT.type_name,
            "case_no": CivilT.reg_no,
            "case_year": CivilT.reg_year,
            "cino": CivilT.cino
        }

        sort_column = sort_columns.get(sort_by, CaseTypeT.type_name)
        order_func = asc if order.lower() == "asc" else desc

        total = query.count()

        register_entries = (
            query
            .order_by(order_func(sort_column))
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        registers = [
            {
                "case_type": row.type_name,
                "case_no": row.reg_no,
                "case_year": row.reg_year,
                "cino": row.cino
            }
            for row in register_entries
        ]

        if not registers:
            return error_response('not_found', f"No cases found for Judge '{judge}'.", status=404)

        response_data = {
            "registers": registers,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            },
            "filters": {
                "search": search,
                "judge": judge,
                "sortBy": sort_by,
                "order": order
            }
        }

        return success_response(
            data=response_data,
            message="Register R6 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R6 entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrsixregisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r6_list_by_court(estcode):
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

        cino = request.args.get("cino", default="", type=str)

        if not cino:
            return error_response(
                error="validation_error",
                message="cino query parameter is required",
                status=400
            )

        db_key = get_cis_db_key(estcode)
        Judge_Name = get_cis_model(db_key, 'judge_name_t')
        DailyProc = get_cis_model(db_key, 'daily_proc')
        CivilT = get_cis_model(db_key, 'civil_t')
        Purpose = get_cis_model(db_key, 'purpose_t')

        query = (
            db.session.query(
                DailyProc.cino.label("cino"),
                CivilT.pet_name.label("pet_name"),
                CivilT.res_name.label("res_name"),
                Purpose.purpose_name.label("purpose_name"),
                DailyProc.next_date.label("next_date"),
                DailyProc.todays_date.label("todays_date"),
                Judge_Name.judge_name.label("judge_name"),
            )
            .select_from(DailyProc)
            .join(CivilT, CivilT.cino == DailyProc.cino)
            .outerjoin(Purpose, DailyProc.purpose_code == Purpose.purpose_code)
            .outerjoin(Judge_Name, DailyProc.jocode == Judge_Name.jocode)
            .filter(DailyProc.cino == cino)
        )

        files = (
            query.order_by(desc(DailyProc.next_date))
            .all()
        )

        registers = [
            {
                "pet_name": row.pet_name,
                "res_name": row.res_name,
                "purpose_name": row.purpose_name,
                "cino": row.cino,
                "next_date": str(row.next_date) if row.next_date else None,
                "todays_date": str(row.todays_date) if row.todays_date else None,
                "judge_name": row.judge_name
            }
            for row in files
        ]

        return success_response(
            data=registers,
            message="Register R6 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R6 entries:" + str(e),
            details=str(e),
            status=500
        )



@register_r_bp.route("/getreightregisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r8_list(estcode):

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
        judge = request.args.get("judge", default="", type=str)

        if page < 1 or limit < 1:
            return error_response(
                error="validation_error",
                message="Page and limit must be greater than 0",
                status=400
            )

        # Sorting
        sort_columns = {
            "created_at": CriminalRegisterREight.created_at,
            "serial_no": CriminalRegisterREight.serial_no,
            "court_name": CriminalRegisterREight.presiding_officer_initial
        }

        sort_column = sort_columns.get(
            sort_by,
            CriminalRegisterREight.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            CriminalRegisterREight.presiding_officer_initial,
            func.count(CriminalRegisterREight.id).label("count")
        )

        # Case type filter
        if judge:
            query = query.filter(
                CriminalRegisterREight.judge.ilike(f"%{judge}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    CriminalRegisterREight.serial_no.ilike(f"%{search}%"),
                    CriminalRegisterREight.witness_name.ilike(f"%{search}%"),
                    CriminalRegisterREight.case_number.ilike(f"%{search}%"),
                    CriminalRegisterREight.attendance_day_1.ilike(f"%{search}%"),
                    CriminalRegisterREight.examined.ilike(f"%{search}%")
                )
            )

        query = query.group_by(CriminalRegisterREight.presiding_officer_initial)

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
                "court_name": row.presiding_officer_initial,
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
                "judge": judge,
                "sortBy": sort_by,
                "order": order
            }
        }

        return success_response(
            data=response_data,
            message="Register R8 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R1 entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/createcriminalreightregister", methods=["POST"])
@jwt_required()
def cri_create_register_r8(estcode):
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
            "serial_no",
            "witness_name",
            "case_number",
            "attendance_day_1",
            "presiding_officer_initial"
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

        register_entry = CriminalRegisterREight(
            serial_no=data.get("serial_no"),
            witness_name=data.get("witness_name"),
            case_number=data.get("case_number"),
            est_code=data.get("est_code"),
            judge=data.get("judge"),
            attendance_day_1=parse_date(
                data.get("attendance_day_1")
            ),
            attendance_day_2=parse_date(
                data.get("attendance_day_2")
            ),
            attendance_day_3=parse_date(
                data.get("attendance_day_3")
            ),
            attendance_day_4=parse_date(
                data.get("attendance_day_4")
            ),
            attendance_day_5=parse_date(
                data.get("attendance_day_5")
            ),
            attendance_day_6=parse_date(
                data.get("attendance_day_6")
            ),
            discharged_day_1=parse_date(
                data.get("discharged_day_1")
            ),
            discharged_day_2=parse_date(
                data.get("attendance_day_6")
            ),
            discharged_day_3=parse_date(
                data.get("discharged_day_3")
            ),
            discharged_after_day_3=parse_date(
                data.get("discharged_after_day_3")
            ),
            examined=data.get("examined"),
            cross_examination_declined=data.get("cross_examination_declined"),
            not_examined=data.get("not_examined"),
            presiding_officer_initial=data.get("presiding_officer_initial"),
            remarks=data.get("remarks"),
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R8",
            entity="criminal_register_r8",
            entity_id=register_entry.id,
            details={
                "serial_no": register_entry.serial_no,
                "presiding_officer_initial": register_entry.presiding_officer_initial,
                "witness_name": register_entry.witness_name,
                "case_number": register_entry.case_number
            }
        )

        return success_response(
            data=register_entry.to_dict(),
            message="Register R8 entry created successfully",
            status=200
        )

    except Exception as e:
        db.session.rollback()

        return error_response(
            error="server_error",
            message="Failed to create Register R8 entry",
            details=str(e),
            status=500
        )


@register_r_bp.route("/getreightregisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_case_details_by_no_yr_r8(estcode):
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

        court_name = request.args.get('court_name')
        judge = request.args.get('judge')

        if not court_name:
            return error_response(
                'validation_error',
                'Court name is required',
                status=400
            )

        query = CriminalRegisterREight.query.filter(CriminalRegisterREight.presiding_officer_initial == court_name)

        files = (
            query.order_by(desc(CriminalRegisterREight.created_at))
            .all()
        )

        if not files:
            return error_response(
                'not_found',
                'Case details not found',
                status=404
            )

        casefile_list = register_r8_schema.dump(files, many=True)

        return success_response(
            data=casefile_list,
            message='Case details fetched successfully',
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R1 entries:" + str(e),
            details=str(e),
            status=500
        )



@register_r_bp.route("/getrthirteenregisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r13_list(estcode):

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
        judge = request.args.get("judge", default="", type=str)

        if page < 1 or limit < 1:
            return error_response(
                error="validation_error",
                message="Page and limit must be greater than 0",
                status=400
            )

        # Sorting
        sort_columns = {
            "created_at": CriminalRegisterRThirteen.created_at,
            "court_name": CriminalRegisterRThirteen.court_name
        }

        sort_column = sort_columns.get(
            sort_by,
            CriminalRegisterRThirteen.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            CriminalRegisterRThirteen.court_name,
            func.count(CriminalRegisterRThirteen.id).label("count")
        )

        # Case type filter
        if judge:
            query = query.filter(
                CriminalRegisterRThirteen.magistrate_name.ilike(f"%{judge}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    CriminalRegisterRThirteen.trial_case_no_year.ilike(f"%{search}%"),
                    CriminalRegisterRThirteen.complainant_name.ilike(f"%{search}%"),
                    CriminalRegisterRThirteen.accused_name.ilike(f"%{search}%"),
                    CriminalRegisterRThirteen.magistrate_name.ilike(f"%{search}%"),
                    CriminalRegisterRThirteen.destruction_date.ilike(f"%{search}%")
                )
            )

        query = query.group_by(CriminalRegisterRThirteen.court_name)

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
                "judge": judge,
                "sortBy": sort_by,
                "order": order
            }
        }

        return success_response(
            data=response_data,
            message="Register R13 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R13 entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/createcriminalrthirteenregister", methods=["POST"])
@jwt_required()
def cri_create_register_r13(estcode):
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
        print(data)

        if not data:
            return error_response(
                error="validation_error",
                message="Request payload is required",
                status=400
            )

        # Required field validation
        required_fields = [
            "est_code",
            "judge",
            "primary_case_no",
            "magistrate_name",
            "trial_case_no_year",
            "complainant_name",
            "accused_name"
        ]

        missing_fields = [
            field for field in required_fields
            if not data.get(field)
        ]

        if missing_fields:
            return error_response(
                error="validation_error",
                message="Required fields are missing" + missing_fields,
                details={
                    "missing_fields": missing_fields
                },
                status=400
            )

        register_entry = CriminalRegisterRThirteen(
            est_code=data.get("est_code"),
            court_name=data.get("magistrate_name"),
            primary_case_no=data.get("primary_case_no"),
            trial_case_no_year=data.get("trial_case_no_year"),
            magistrate_name=data.get("judge"),
            complainant_name=data.get("complainant_name"),
            accused_name=data.get("accused_name"),
            final_order_details=data.get("final_order_details"),
            appeal_revision_result=data.get("appeal_revision_result"),
            file_class=data.get("file_class"),
            disposed_shelved_date=parse_date(data.get("disposed_shelved_date")),
            shelf_rack_no=data.get("shelf_rack_no"),
            destruction_date=parse_date(data.get("destruction_date")),
            remarks=data.get("remarks"),
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R13",
            entity="criminal_register_r13",
            entity_id=register_entry.id,
            details={
                "primary_case_no": register_entry.primary_case_no,
                "magistrate_name": register_entry.magistrate_name,
                "court_name": register_entry.court_name,
                "complainant_name": register_entry.complainant_name,
                "accused_name": register_entry.accused_name
            }
        )

        return success_response(
            data=register_entry.to_dict(),
            message="Register R13 entry created successfully",
            status=200
        )

    except Exception as e:
        db.session.rollback()

        return error_response(
            error="server_error",
            message="Failed to create Register R13 entry",
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrthirteenregisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_case_details_by_no_yr_r13(estcode):
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

        court_name = request.args.get('court_name')
        judge = request.args.get('judge')

        if not court_name:
            return error_response(
                'validation_error',
                'Court name is required',
                status=400
            )

        query = CriminalRegisterRThirteen.query.filter(CriminalRegisterRThirteen.court_name == court_name)

        files = (
            query.order_by(desc(CriminalRegisterRThirteen.created_at))
            .all()
        )

        if not files:
            return error_response(
                'not_found',
                'Case details not found',
                status=404
            )

        casefile_list = criminal_register_r13_schema.dump(files, many=True)

        return success_response(
            data=casefile_list,
            message='Case details fetched successfully',
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R1 entries:" + str(e),
            details=str(e),
            status=500
        )

