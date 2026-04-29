from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import func, cast, String
from sqlalchemy.sql.operators import or_
from sqlalchemy.sql.selectable import and_

from app.models.casefile.casefile_uploads import CaseFileHeader
from app.utils import error_response, success_response

search_bp = Blueprint('search_bp', __name__)


def build_case_string(case_type, case_no, case_year):
    return (
            case_type
            + ' '
            + cast(case_no, String)
            + '/'
            + cast(case_year, String)
    )


@search_bp.route("/parameterwise", methods=['GET'])
def search():
    q = request.args.get("q", "").strip()

    if not q:
        return error_response(status=404, error='invalid_data', message='Input Error')

    pattern = f"%{q}%"

    reg_string = build_case_string(
        CaseFileHeader.reg_case_type,
        CaseFileHeader.reg_case_no,
        CaseFileHeader.reg_case_year
    )

    cis_string = build_case_string(
        CaseFileHeader.cis_case_type,
        CaseFileHeader.cis_case_no,
        CaseFileHeader.cis_case_year
    )

    rows = (
        CaseFileHeader.query
        .filter(
            CaseFileHeader.cino.ilike(pattern) |
            reg_string.ilike(pattern) |
            CaseFileHeader.reg_case_type.ilike(pattern) |
            cast(CaseFileHeader.reg_case_no, String).ilike(pattern) |
            cast(CaseFileHeader.reg_case_year, String).ilike(pattern) |
            cis_string.ilike(pattern) |
            CaseFileHeader.cis_case_type.ilike(pattern) |
            cast(CaseFileHeader.cis_case_no, String).ilike(pattern) |
            cast(CaseFileHeader.cis_case_year, String).ilike(pattern)
        )
        .limit(15)
        .all()
    )

    results = []

    for r in rows:
        results.append({
            "id": r.id,
            "cino": r.cino,
            "reg_case": f"{r.reg_case_type} {r.reg_case_no}/{r.reg_case_year}",
            "cis_case": f"{r.cis_case_type} {r.cis_case_no}/{r.cis_case_year}",
            "reg_case_type": r.reg_case_type,
            "reg_case_no": r.reg_case_no,
            "reg_case_year": r.reg_case_year,
            "cis_case_type": r.cis_case_type,
            "cis_case_no": r.cis_case_no,
            "cis_case_year": r.cis_case_year
        })

    if not results:
        return error_response(status=404, error='invalid_data', message='Case-file not found or Invalid Input data')

    return success_response(status=200, message='Case-file search successfully', data=results)


@search_bp.route("/parameterwisebyjudge", methods=['GET'])
def search_by_judge():
    q = request.args.get("q", "").strip()
    judge = request.args.get("judge")

    if not q:
        return error_response(status=404, error='invalid_data', message='Input Error')

    if not judge:
        return error_response(status=404, error='invalid_judge', message='Judge name is not mention')

    pattern = f"%{q}%"

    reg_string = build_case_string(
        CaseFileHeader.reg_case_type,
        CaseFileHeader.reg_case_no,
        CaseFileHeader.reg_case_year
    )

    cis_string = build_case_string(
        CaseFileHeader.cis_case_type,
        CaseFileHeader.cis_case_no,
        CaseFileHeader.cis_case_year
    )

    rows = (
        CaseFileHeader.query
        .filter(
            CaseFileHeader.cino.ilike(pattern) |
            reg_string.ilike(pattern) |
            CaseFileHeader.reg_case_type.ilike(pattern) |
            cast(CaseFileHeader.reg_case_no, String).ilike(pattern) |
            cast(CaseFileHeader.reg_case_year, String).ilike(pattern) |
            cis_string.ilike(pattern) |
            CaseFileHeader.cis_case_type.ilike(pattern) |
            cast(CaseFileHeader.cis_case_no, String).ilike(pattern) |
            cast(CaseFileHeader.cis_case_year, String).ilike(pattern) &
            CaseFileHeader.judge.ilike(judge)
        )
        .limit(15)
        .all()
    )

    results = []

    for r in rows:
        results.append({
            "id": r.id,
            "cino": r.cino,
            "reg_case": f"{r.reg_case_type} {r.reg_case_no}/{r.reg_case_year}",
            "cis_case": f"{r.cis_case_type} {r.cis_case_no}/{r.cis_case_year}",
            "reg_case_type": r.reg_case_type,
            "reg_case_no": r.reg_case_no,
            "reg_case_year": r.reg_case_year,
            "cis_case_type": r.cis_case_type,
            "cis_case_no": r.cis_case_no,
            "cis_case_year": r.cis_case_year
        })

    if not results:
        return error_response(status=404, error='invalid_data', message='Case-file not found or Invalid Input data')

    return success_response(status=200, message='Case-file search successfully', data=results)


@search_bp.route("/optionwisesearch", methods=['GET'])
def search_option_wise():
    casetype = request.args.get("casetype", "").strip()
    caseno = request.args.get("caseno", "").strip()
    caseyear = request.args.get("caseyear", "").strip()

    if not casetype or not caseno or not caseyear:
        return error_response(
            status=404,
            error='invalid_data',
            message='Input Error: Missing case type, case no, or case year'
        )

    try:
        ct_like = f"%{casetype}%"
        no_like = f"%{caseno}%"
        yr_like = f"%{caseyear}%"

        rows = (
            CaseFileHeader.query.filter(
                # (REG matches ALL inputs) OR (CIS matches ALL inputs)
                or_(
                    and_(
                        CaseFileHeader.reg_case_type.ilike(ct_like),
                        cast(CaseFileHeader.reg_case_no, String).ilike(no_like),
                        cast(CaseFileHeader.reg_case_year, String).ilike(yr_like)
                    ),
                    and_(
                        CaseFileHeader.cis_case_type.ilike(ct_like),
                        cast(CaseFileHeader.cis_case_no, String).ilike(no_like),
                        cast(CaseFileHeader.cis_case_year, String).ilike(yr_like)
                    )
                )
            )
            .limit(15)
            .all()
        )

        if not rows:
            return error_response(
                status=404,
                error='not_found',
                message='No case-file found for given inputs'
            )

        results = [
            {
                "id": r.id,
                "cino": r.cino,
                "reg_case": f"{r.reg_case_type} {r.reg_case_no}/{r.reg_case_year}",
                "cis_case": f"{r.cis_case_type} {r.cis_case_no}/{r.cis_case_year}",
                "reg_case_type": r.reg_case_type,
                "reg_case_no": r.reg_case_no,
                "reg_case_year": r.reg_case_year,
                "cis_case_type": r.cis_case_type,
                "cis_case_no": r.cis_case_no,
                "cis_case_year": r.cis_case_year
            }
            for r in rows
        ]

        return success_response(status=200, message='Case-file search successfully', data=results)
    except Exception as e:
        current_app.logger.exception("Error during case-file search")
        return error_response(
            status=500,
            error='server_error',
            message='Internal server error'
        )


@search_bp.route("/optionwisesearchbycino", methods=['GET'])
def search_option_wise_cino():
    cino = request.args.get("cino", "").strip()

    if not cino:
        return error_response(
            status=404,
            error='invalid_data',
            message='Input Error: Missing case type, case no, or case year'
        )

    try:
        ct_like = f"%{cino}%"

        rows = (
            CaseFileHeader.query.filter(
                # (REG matches ALL inputs) OR (CIS matches ALL inputs)
                CaseFileHeader.cino.ilike(ct_like)
            )
            .limit(15)
            .all()
        )

        if not rows:
            return error_response(
                status=404,
                error='not_found',
                message='No case-file found for given inputs'
            )

        results = [
            {
                "id": r.id,
                "cino": r.cino,
                "reg_case": f"{r.reg_case_type} {r.reg_case_no}/{r.reg_case_year}",
                "cis_case": f"{r.cis_case_type} {r.cis_case_no}/{r.cis_case_year}",
                "reg_case_type": r.reg_case_type,
                "reg_case_no": r.reg_case_no,
                "reg_case_year": r.reg_case_year,
                "cis_case_type": r.cis_case_type,
                "cis_case_no": r.cis_case_no,
                "cis_case_year": r.cis_case_year
            }
            for r in rows
        ]

        return success_response(status=200, message='Case-file search successfully', data=results)
    except Exception as e:
        current_app.logger.exception("Error during case-file search")
        return error_response(
            status=500,
            error='server_error',
            message='Internal server error'
        )


@search_bp.route("/semantic", methods=['GET'])
def search_semantic():
    q = request.args.get("q", "").strip()

    if not q:
        return error_response(status=404, error='invalid_data', message='Input Error')

    pattern = f"%{q}%"

    reg_string = build_case_string(
        CaseFileHeader.reg_case_type,
        CaseFileHeader.reg_case_no,
        CaseFileHeader.reg_case_year
    )

    cis_string = build_case_string(
        CaseFileHeader.cis_case_type,
        CaseFileHeader.cis_case_no,
        CaseFileHeader.cis_case_year
    )

    rows = (
        CaseFileHeader.query
        .filter(
            CaseFileHeader.cino.ilike(pattern) |
            reg_string.ilike(pattern) |
            CaseFileHeader.reg_case_type.ilike(pattern) |
            cast(CaseFileHeader.reg_case_no, String).ilike(pattern) |
            cast(CaseFileHeader.reg_case_year, String).ilike(pattern) |
            cis_string.ilike(pattern) |
            CaseFileHeader.cis_case_type.ilike(pattern) |
            cast(CaseFileHeader.cis_case_no, String).ilike(pattern) |
            cast(CaseFileHeader.cis_case_year, String).ilike(pattern)
        )
        .limit(15)
        .all()
    )

    results = []

    for r in rows:
        results.append({
            "id": r.id,
            "cino": r.cino,
            "reg_case": f"{r.reg_case_type} {r.reg_case_no}/{r.reg_case_year}",
            "cis_case": f"{r.cis_case_type} {r.cis_case_no}/{r.cis_case_year}",
            "reg_case_type": r.reg_case_type,
            "reg_case_no": r.reg_case_no,
            "reg_case_year": r.reg_case_year,
            "cis_case_type": r.cis_case_type,
            "cis_case_no": r.cis_case_no,
            "cis_case_year": r.cis_case_year
        })

    if not results:
        return error_response(status=404, error='invalid_data', message='Case-file not found or Invalid Input data')

    return success_response(status=200, message='Case-file search successfully', data=results)