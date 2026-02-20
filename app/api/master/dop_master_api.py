from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_

from app.estcode_db import get_cis_db_key
from app.extensions import db
from app.models.cis.registry import get_cis_model
from app.models.master.case_type_t import CaseTypeT
from app.models.master.designation import DesignationName
from app.models.master.judge import Judge_Name
from app.models.master.judge_t import JudgeWithCourtNo
from app.utils import error_response, success_response

dop_master_bp = Blueprint('dop_master_bp', __name__)


@dop_master_bp.route('/judges', methods=['GET'])
def get_cis_judge():
    try:
        judge_with_designation = (
            db.session.query(Judge_Name, DesignationName)
            .join(DesignationName, Judge_Name.desg_code == DesignationName.desgcode)
            .join(JudgeWithCourtNo, Judge_Name.jocode == JudgeWithCourtNo.jocode)
            .filter(
                and_(
                    JudgeWithCourtNo.display == 'Y',
                    JudgeWithCourtNo.from_dt.isnot(None),
                    JudgeWithCourtNo.to_dt.is_(None)
                )
            )
            .all()
        )

        result = []

        for j, d in judge_with_designation:
            data = j.to_dict()
            data['desgname'] = d.desgname
            result.append(data)

        if not result:
            return error_response(
                error='no_judges',
                message='No active judges found',
                status=404
            )

        return success_response(
            data=result,
            message='Judges fetched successfully'
        )
    except Exception:
        current_app.logger.exception('Error fetching judges')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@dop_master_bp.route('/jd/getjudgemaster', methods=['GET'])
@jwt_required()
def get_cis_judge_master(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        db_key = get_cis_db_key(estcode)
        JudgeName = get_cis_model(db_key, 'judge_name_t')
        Designation = get_cis_model(db_key, 'desg_t')
        JudgeWithCourt = get_cis_model(db_key, 'judge_t')

        judge_with_designation = (
            db.session.query(JudgeName, Designation, JudgeWithCourt)
            .join(JudgeWithCourt, JudgeName.jocode == JudgeWithCourt.jocode)
            .join(Designation, JudgeWithCourt.desg_code == Designation.desgcode)
            .filter(
                and_(
                    JudgeWithCourt.display == 'Y',
                    JudgeWithCourt.from_dt.isnot(None),
                    JudgeWithCourt.to_dt.is_(None)
                )
            )
            .order_by(
                JudgeWithCourt.court_no.asc()
            )
            .all()
        )

        result = []

        for j, d, c in judge_with_designation:
            data = j.to_dict()
            data['desgname'] = d.desgname
            data['court_no'] = c.court_no
            result.append(data)

        if not result:
            return error_response(
                error='no_judges',
                message='No active judges found',
                status=404
            )

        return success_response(
            data=result,
            message='Judges fetched successfully'
        )
    except Exception:
        current_app.logger.exception('Error fetching judges')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@dop_master_bp.route('/ct/getcasetypemaster', methods=['GET'])
@jwt_required()
def get_cis_casetype_master():
    try:
        case_types = CaseTypeT.query.filter_by(display='Y').all()

        if not case_types:
            return error_response(
                error='no_casetype',
                message='No case types found',
                status=404
            )

        result = [ct.to_dict() for ct in case_types]

        return success_response(
            data=result,
            message='Casetype fetched successfully'
        )
    except Exception:
        current_app.logger.exception('Error fetching judges')
        return error_response('server_error', 'An unexpected error occurred', status=500)