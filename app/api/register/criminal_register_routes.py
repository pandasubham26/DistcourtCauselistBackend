from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from sqlalchemy import asc, desc, func, or_, and_

from app.estcode_db import get_cis_db_key
from app.extensions import db
from app.models.cis.registry import get_cis_model
from app.models.register.criminal_register_model import CriminalRegisterROne, CriminalRegisterRThree, \
    CriminalRegisterREight, CriminalRegisterRThirteen, CriminalRegisterRSeven, CriminalRegisterRTwo, \
    CriminalRegisterRNineA, CriminalRegisterRTenA, CriminalRegisterRThirteenA
from app.schemas.criminal_r_eight_register_schema import register_r8_schema
from app.schemas.criminal_r_one_register_schema import criminal_register_r_one_schema
from app.schemas.criminal_r_seven_schema import register_r7_schema
from app.schemas.criminal_r_thirteen_register_schema import criminal_register_r13_schema
from app.schemas.criminal_r_three_register_schema import criminal_register_r_three_schema
from app.schemas.criminal_register_r10a_schema import criminal_register_r10a_schema
from app.schemas.criminal_register_r2_schema import criminal_register_r_two_schema
from app.schemas.criminal_register_r9a_schema import criminal_register_r9a_schema
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


@register_r_bp.route("/getsevenregisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r7_list(estcode):

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
            "created_at": CriminalRegisterRSeven.created_at,
            "date": CriminalRegisterRSeven.date
        }

        sort_column = sort_columns.get(
            sort_by,
            CriminalRegisterRSeven.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            CriminalRegisterRSeven.date,
            func.count(CriminalRegisterRSeven.id).label("count")
        )

        # Case type filter
        if judge:
            query = query.filter(
                CriminalRegisterRSeven.judge.ilike(f"%{judge}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    CriminalRegisterRSeven.serial_no.ilike(f"%{search}%"),
                    CriminalRegisterRSeven.date.ilike(f"%{search}%"),
                    CriminalRegisterRSeven.nature_of_documents.ilike(f"%{search}%"),
                    CriminalRegisterRSeven.case_number.ilike(f"%{search}%"),
                )
            )

        query = query.group_by(CriminalRegisterRSeven.date)

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
                "date": row.date,
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
            message="Register R7 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R7 entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/createcriminalsevenregister", methods=["POST"])
@jwt_required()
def cri_create_register_r7(estcode):
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
            "nature_of_documents",
            "date",
            "case_number",
            "est_code",
            "judge",
            "court_name",
            "process_fee_rs",
            "process_fee_ps"
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

        register_entry = CriminalRegisterRSeven(
            serial_no=data.get("serial_no"),
            nature_of_documents=data.get("nature_of_documents"),
            case_number=data.get("case_number"),
            est_code=data.get("est_code"),
            judge=data.get("judge"),
            court_name=data.get("court_name"),
            process_fee_rs=data.get("process_fee_rs"),
            process_fee_ps=data.get("process_fee_ps"),
            affidavit_fee_rs=data.get("affidavit_fee_rs"),
            affidavit_fee_ps=data.get("affidavit_fee_ps"),
            date=parse_date(data.get("date")),
            other_fee_rs=data.get("other_fee_rs"),
            other_fee_ps=data.get("other_fee_ps"),
            remarks=data.get("remarks"),
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R7",
            entity="criminal_register_r7",
            entity_id=register_entry.id,
            details={
                "serial_no": register_entry.serial_no,
                "nature_of_documents": register_entry.nature_of_documents,
                "judge": register_entry.judge,
                "court_name": register_entry.court_name,
                "case_number": register_entry.case_number,
                "process_fee_rs": register_entry.process_fee_rs
            }
        )

        return success_response(
            data=register_entry.to_dict(),
            message="Register R7 entry created successfully",
            status=200
        )

    except Exception as e:
        db.session.rollback()

        return error_response(
            error="server_error",
            message="Failed to create Register R7 entry",
            details=str(e),
            status=500
        )


@register_r_bp.route("/getsevenregisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_case_details_by_no_yr_r7(estcode):
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

        date = request.args.get('date')
        judge = request.args.get('judge')

        if not date:
            return error_response(
                'validation_error',
                'Date is required',
                status=400
            )

        query = CriminalRegisterRSeven.query.filter(CriminalRegisterRSeven.date == date)

        if not judge:
            return error_response(
                'validation_error',
                'Judge is required',
                status=400
            )
        query = CriminalRegisterRSeven.query.filter(CriminalRegisterRSeven.judge == judge)
        files = (
            query.order_by(asc(CriminalRegisterRSeven.created_at))
            .all()
        )

        if not files:
            return error_response(
                'not_found',
                'Case details not found',
                status=404
            )

        casefile_list = register_r7_schema.dump(files, many=True)

        return success_response(
            data=casefile_list,
            message='Case details fetched successfully',
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R7 entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrtworegisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r2_list(estcode):

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
            "created_at": CriminalRegisterRTwo.created_at,
            "court_name": CriminalRegisterRTwo.court_name
        }

        sort_column = sort_columns.get(
            sort_by,
            CriminalRegisterRTwo.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            CriminalRegisterRTwo.court_name,
            func.count(CriminalRegisterRTwo.id).label("count")
        )

        # Case type filter
        if judge:
            query = query.filter(
                CriminalRegisterRTwo.auth_judge.ilike(f"%{judge}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    CriminalRegisterRTwo.serial_no.ilike(f"%{search}%"),
                    CriminalRegisterRTwo.party_names.ilike(f"%{search}%"),
                    CriminalRegisterRTwo.crime_information.ilike(f"%{search}%"),
                    CriminalRegisterRTwo.police_station.ilike(f"%{search}%"),
                )
            )

        query = query.group_by(CriminalRegisterRTwo.court_name)

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
            message="Register R2 entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R2 entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/createcriminalrtworegister", methods=["POST"])
@jwt_required()
def cri_create_register_r2(estcode):
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
            "case_no",
            "police_station",
            "receipt_date",
            "auth_estcode",
            "auth_judge",
            "court_name",
            "party_names",
            "police_investigation_return",
            "crime_information"
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

        register_entry = CriminalRegisterRTwo(
            court_name=data.get("court_name"),
            case_no=data.get("case_no"),
            auth_estcode=data.get("auth_estcode"),
            auth_judge=data.get("auth_judge"),
            serial_no=data.get("serial_no"),
            police_station=data.get("police_station"),
            receipt_date=parse_date(data.get("receipt_date")),
            crime_information=data.get("crime_information"),
            party_names=data.get('party_names'),
            police_investigation_return=data.get("police_investigation_return"),
            preliminary_order=data.get('preliminary_order'),
            final_order=data.get('final_order'),
            remarks=data.get("remarks"),
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R2",
            entity="criminal_register_r2",
            entity_id=register_entry.id,
            details={
                "serial_no": register_entry.serial_no,
                "police_station": register_entry.police_station,
                "judge": register_entry.auth_judge,
                "court_name": register_entry.court_name,
                "case_number": register_entry.case_no,
                "crime_information": register_entry.crime_information,
                "party_names": register_entry.party_names
            }
        )

        return success_response(
            data=register_entry.to_dict(),
            message="Register R2 entry created successfully",
            status=200
        )

    except Exception as e:
        db.session.rollback()

        return error_response(
            error="server_error",
            message="Failed to create Register R2 entry",
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrtworegisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_case_details_by_no_yr_r2(estcode):
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

        query = CriminalRegisterRTwo.query.filter(CriminalRegisterRTwo.court_name == court_name)

        if not judge:
            return error_response(
                'validation_error',
                'Judge is required',
                status=400
            )
        query = CriminalRegisterRTwo.query.filter(CriminalRegisterRTwo.auth_judge == judge)
        files = (
            query.order_by(asc(CriminalRegisterRTwo.created_at))
            .all()
        )

        if not files:
            return error_response(
                'not_found',
                'Case details not found',
                status=404
            )

        casefile_list = criminal_register_r_two_schema.dump(files, many=True)

        return success_response(
            data=casefile_list,
            message='Case details fetched successfully',
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R2 entries:" + str(e),
            details=str(e),
            status=500
        )



@register_r_bp.route("/getrninearegisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r9a_list(estcode):

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
            "created_at": CriminalRegisterRNineA.created_at,
            "court_name": CriminalRegisterRNineA.court_name
        }

        sort_column = sort_columns.get(
            sort_by,
            CriminalRegisterRNineA.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            CriminalRegisterRNineA.court_name,
            func.count(CriminalRegisterRNineA.id).label("count")
        )

        # Case type filter
        if judge:
            query = query.filter(
                CriminalRegisterRNineA.auth_judge.ilike(f"%{judge}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    CriminalRegisterRNineA.serial_no.ilike(f"%{search}%"),
                    CriminalRegisterRNineA.person_name.ilike(f"%{search}%"),
                    CriminalRegisterRNineA.issue_date.ilike(f"%{search}%"),
                    CriminalRegisterRNineA.returnable_date.ilike(f"%{search}%"),
                )
            )

        query = query.group_by(CriminalRegisterRNineA.court_name)

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
            message="Register R9A entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R9A entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/createcriminalrninearegister", methods=["POST"])
@jwt_required()
def cri_create_register_r9a(estcode):
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
            "case_no",
            "court_name",
            "person_name",
            "auth_estcode",
            "auth_judge",
            "nature_of_process",
            "issue_date",
            "returnable_date",
            "receiver_date"
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

        register_entry = CriminalRegisterRNineA(
            court_name=data.get("court_name"),
            case_no=data.get("case_no"),
            auth_estcode=data.get("auth_estcode"),
            auth_judge=data.get("auth_judge"),
            serial_no=data.get("serial_no"),
            person_name=data.get("person_name"),
            nature_of_process=data.get("nature_of_process"),
            issue_date=parse_date(data.get("issue_date")),
            returnable_date=parse_date(data.get("returnable_date")),
            receiver_date=parse_date(data.get("receiver_date")),
            return_date=parse_date(data.get("return_date")),
            remarks=data.get("remarks"),
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R9A",
            entity="criminal_register_r9a",
            entity_id=register_entry.id,
            details={
                "serial_no": register_entry.serial_no,
                "person_name": register_entry.person_name,
                "judge": register_entry.auth_judge,
                "court_name": register_entry.court_name,
                "case_number": register_entry.case_no,
                "issue_date": register_entry.issue_date,
                "returnable_date": register_entry.returnable_date
            }
        )

        return success_response(
            data=register_entry.to_dict(),
            message="Register R9A entry created successfully",
            status=200
        )

    except Exception as e:
        db.session.rollback()

        return error_response(
            error="server_error",
            message="Failed to create Register R9A entry",
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrninearegisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_case_details_by_no_yr_r9a(estcode):
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

        query = CriminalRegisterRNineA.query.filter(CriminalRegisterRNineA.court_name == court_name)

        if not judge:
            return error_response(
                'validation_error',
                'Judge is required',
                status=400
            )
        query = CriminalRegisterRNineA.query.filter(CriminalRegisterRNineA.auth_judge == judge)
        files = (
            query.order_by(asc(CriminalRegisterRNineA.created_at))
            .all()
        )

        if not files:
            return error_response(
                'not_found',
                'Case details not found',
                status=404
            )

        casefile_list = criminal_register_r9a_schema.dump(files, many=True)

        return success_response(
            data=casefile_list,
            message='Case details fetched successfully',
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R9A entries:" + str(e),
            details=str(e),
            status=500
        )



@register_r_bp.route("/getrtenaregisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r10a_list(estcode):

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
            "created_at": CriminalRegisterRTenA.created_at,
            "court_name": CriminalRegisterRTenA.court_name
        }

        sort_column = sort_columns.get(
            sort_by,
            CriminalRegisterRTenA.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            CriminalRegisterRTenA.court_name,
            func.count(CriminalRegisterRTenA.id).label("count")
        )

        # Case type filter
        if judge:
            query = query.filter(
                CriminalRegisterRTenA.auth_judge.ilike(f"%{judge}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    CriminalRegisterRTenA.serial_no.ilike(f"%{search}%"),
                    CriminalRegisterRTenA.case_no.ilike(f"%{search}%"),
                    CriminalRegisterRTenA.issue_date.ilike(f"%{search}%"),
                )
            )

        query = query.group_by(CriminalRegisterRTenA.court_name)

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
            message="Register R10A entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R9A entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/createcriminalrtenaregister", methods=["POST"])
@jwt_required()
def cri_create_register_r10a(estcode):
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
            "case_no",
            "court_name",
            "auth_estcode",
            "auth_judge",
            "trail_date",
            "prosecution_witnesses",
            "issue_date",
            "mode_of_service",
            "return_date"
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

        register_entry = CriminalRegisterRTenA(
            auth_estcode=data.get("auth_estcode"),
            auth_judge=data.get("auth_judge"),
            court_name=data.get("court_name"),
            serial_no=data.get("serial_no"),
            case_no=data.get("case_no"),
            trail_date=parse_date(data.get("trail_date")),
            prosecution_witnesses=data.get("prosecution_witnesses"),
            issue_date=parse_date(data.get("issue_date")),
            mode_of_service=data.get("mode_of_service"),
            return_date=parse_date(data.get("return_date")),
            suf_insuff=data.get("suf_insuff"),
            step_taken=data.get("step_taken"),
            remarks=data.get("remarks"),
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R10A",
            entity="criminal_register_r10a",
            entity_id=register_entry.id,
            details={
                "serial_no": register_entry.serial_no,
                "prosecution_witnesses": register_entry.prosecution_witnesses,
                "judge": register_entry.auth_judge,
                "court_name": register_entry.court_name,
                "case_number": register_entry.case_no,
                "issue_date": register_entry.issue_date,
                "return_date": register_entry.return_date
            }
        )

        return success_response(
            data=register_entry.to_dict(),
            message="Register R10A entry created successfully",
            status=200
        )

    except Exception as e:
        db.session.rollback()
        print(str(e))

        return error_response(
            error="server_error",
            message="Failed to create Register R10A entry" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrtenaregisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_case_details_by_no_yr_r10a(estcode):
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

        query = CriminalRegisterRTenA.query.filter(CriminalRegisterRTenA.court_name == court_name)

        if not judge:
            return error_response(
                'validation_error',
                'Judge is required',
                status=400
            )
        query = CriminalRegisterRTenA.query.filter(CriminalRegisterRTenA.auth_judge == judge)
        files = (
            query.order_by(asc(CriminalRegisterRTenA.created_at))
            .all()
        )

        if not files:
            return error_response(
                'not_found',
                'Case details not found',
                status=404
            )

        casefile_list = criminal_register_r10a_schema.dump(files, many=True)

        return success_response(
            data=casefile_list,
            message='Case details fetched successfully',
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R9A entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrthirteenaregisterlist", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_register_r13a_list(estcode):

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
            "created_at": CriminalRegisterRThirteenA.created_at,
            "court_name": CriminalRegisterRThirteenA.court_name
        }

        sort_column = sort_columns.get(
            sort_by,
            CriminalRegisterRThirteenA.created_at
        )

        order_func = asc if order.lower() == "asc" else desc

        query = db.session.query(
            CriminalRegisterRThirteenA.court_name,
            func.count(CriminalRegisterRThirteenA.id).label("count")
        )

        # Case type filter
        if judge:
            query = query.filter(
                CriminalRegisterRThirteenA.auth_judge.ilike(f"%{judge}%")
            )

        # Search filter
        if search:
            query = query.filter(
                or_(
                    CriminalRegisterRThirteenA.serial_no.ilike(f"%{search}%"),
                    CriminalRegisterRThirteenA.case_no.ilike(f"%{search}%"),
                    CriminalRegisterRThirteenA.issue_date.ilike(f"%{search}%"),
                )
            )

        query = query.group_by(CriminalRegisterRThirteenA.court_name)

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
            message="Register R13A entries retrieved successfully",
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R13A entries:" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/createcriminalrthirteenaregister", methods=["POST"])
@jwt_required()
def cri_create_register_r13a(estcode):
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
            "case_no",
            "court_name",
            "auth_estcode",
            "auth_judge",
            "trail_date",
            "prosecution_witnesses",
            "issue_date",
            "mode_of_service",
            "return_date"
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

        register_entry = CriminalRegisterRTenA(
            auth_estcode=data.get("auth_estcode"),
            auth_judge=data.get("auth_judge"),
            court_name=data.get("court_name"),
            serial_no=data.get("serial_no"),
            case_no=data.get("case_no"),
            trail_date=parse_date(data.get("trail_date")),
            prosecution_witnesses=data.get("prosecution_witnesses"),
            issue_date=parse_date(data.get("issue_date")),
            mode_of_service=data.get("mode_of_service"),
            return_date=parse_date(data.get("return_date")),
            suf_insuff=data.get("suf_insuff"),
            step_taken=data.get("step_taken"),
            remarks=data.get("remarks"),
        )

        db.session.add(register_entry)
        db.session.commit()

        # Audit logging
        log_action(
            actor_user_id=user_id,
            action="CREATE_REGISTER_R10A",
            entity="criminal_register_r10a",
            entity_id=register_entry.id,
            details={
                "serial_no": register_entry.serial_no,
                "prosecution_witnesses": register_entry.prosecution_witnesses,
                "judge": register_entry.auth_judge,
                "court_name": register_entry.court_name,
                "case_number": register_entry.case_no,
                "issue_date": register_entry.issue_date,
                "return_date": register_entry.return_date
            }
        )

        return success_response(
            data=register_entry.to_dict(),
            message="Register R10A entry created successfully",
            status=200
        )

    except Exception as e:
        db.session.rollback()
        print(str(e))

        return error_response(
            error="server_error",
            message="Failed to create Register R10A entry" + str(e),
            details=str(e),
            status=500
        )


@register_r_bp.route("/getrthirteenaregisterlistbycourt", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def get_case_details_by_no_yr_r13a(estcode):
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

        query = CriminalRegisterRTenA.query.filter(CriminalRegisterRTenA.court_name == court_name)

        if not judge:
            return error_response(
                'validation_error',
                'Judge is required',
                status=400
            )
        query = CriminalRegisterRTenA.query.filter(CriminalRegisterRTenA.auth_judge == judge)
        files = (
            query.order_by(asc(CriminalRegisterRTenA.created_at))
            .all()
        )

        if not files:
            return error_response(
                'not_found',
                'Case details not found',
                status=404
            )

        casefile_list = criminal_register_r10a_schema.dump(files, many=True)

        return success_response(
            data=casefile_list,
            message='Case details fetched successfully',
            status=200
        )

    except Exception as e:
        return error_response(
            error="server_error",
            message="Failed to retrieve Register R9A entries:" + str(e),
            details=str(e),
            status=500
        )

