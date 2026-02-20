from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import and_, func, cast, Integer

from app.estcode_db import get_cis_db_key
from app.extensions import db
from app.models.causelist.causelist import CauseList
from app.models.cis.registry import get_cis_model
from app.utils import error_response, success_response

causelist_bp = Blueprint('causelist_bp', __name__)


@causelist_bp.route('/cl/generate', methods=['GET'])
@jwt_required()
def generate_causelist(estcode):
    jwt_estcode = get_jwt().get('estcode')
    if jwt_estcode != estcode:
        return error_response(
            'forbidden',
            'Invalid establishment code',
            status=403
        )

    date = request.args.get('date')
    judge = request.args.get('judge')
    type = request.args.get('type')

    db_key = get_cis_db_key(estcode)
    Judge_Name = get_cis_model(db_key, 'judge_name_t')
    JudgeWithCourtNo = get_cis_model(db_key, 'judge_t')
    DailyProc = get_cis_model(db_key, 'daily_proc')
    PurposeT = get_cis_model(db_key, 'purpose_t')
    CivilT = get_cis_model(db_key, 'civil_t')
    CaseTypeT = get_cis_model(db_key, 'case_type_t')

    if not date or not judge or not type:
        return error_response('missing_parameters', "Both 'date' and 'judge' and 'type' are required parameters.", status=400)

    # Find judge code
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
    print(court_no)

    # Fetch cases from base tables
    query = (
        db.session.query(
            DailyProc.srno,
            DailyProc.next_date,
            CaseTypeT.type_name,
            CivilT.reg_no,
            CivilT.reg_year,
            PurposeT.purpose_name,
            PurposeT.purpose_priority,
            CivilT.pet_name,
            CivilT.res_name,
            CivilT.pet_adv,
            CivilT.res_adv,
            CaseTypeT.type_flag
        )
        .select_from(CivilT)
        .join(JudgeWithCourtNo, CivilT.court_no == JudgeWithCourtNo.court_no)
        .outerjoin(DailyProc, DailyProc.cino == CivilT.cino)
        .join(PurposeT, CivilT.purpose_next == PurposeT.purpose_code)
        .join(CaseTypeT, CaseTypeT.case_type == CivilT.regcase_type)
        .filter(
            and_(
                # DailyProc.next_date == date,
                CivilT.date_next_list == date,
                CaseTypeT.type_flag == type,
                CivilT.court_no == court_no

            )
        )
        .order_by(PurposeT.purpose_priority)
    )

    results = query.all()

    if not results:
        return error_response('not_found', f"No cases found for Judge '{judge}' on {date}.", status=404)

    inserted = 0
    skipped = 0

    for r in results:
        existing = (
            db.session.query(CauseList)
            .filter(
                and_(
                    CauseList.date == date,
                    CauseList.judge_name == judge,
                    CauseList.casetype == r.type_name,
                    CauseList.casenumber == r.reg_no,
                    CauseList.caseyear == r.reg_year,
                    CauseList.purposename == r.purpose_name,
                    CauseList.type_flag == type
                )
            )
            .first()
        )

        if existing:
            skipped += 1
            continue

        entry = CauseList(
            date=date,
            next_date=r.next_date,
            judge_name=judge,
            casetype=r.type_name,
            casenumber=r.reg_no,
            caseyear=r.reg_year,
            purposename=r.purpose_name,
            purpose_priority=r.purpose_priority,
            petname=r.pet_name,
            resname=r.res_name,
            petadv=r.pet_adv,
            resadv=r.res_adv,
            srno=r.srno,
            type_flag=r.type_flag
        )
        db.session.add(entry)
        inserted += 1

    db.session.commit()

    # ✅ Always return full data for that judge/date (even if no new inserts)
    all_records = (
        db.session.query(CauseList)
        .filter(
            and_(
                CauseList.date == date,
                CauseList.judge_name == judge,
                CauseList.type_flag == type
            )
        )
        .order_by(CauseList.purpose_priority,
                  CauseList.caseyear.asc(),
                  CauseList.casenumber.asc()
                  )
        .all()
    )

    data = [
        {
            "casetype": r.casetype,
            "casenumber": r.casenumber,
            "caseyear": r.caseyear,
            "purposename": r.purposename,
            "petname": r.petname,
            "resname": r.resname,
            "petadv": r.petadv,
            "resadv": r.resadv,
            "srno": r.srno
        }
        for r in all_records
    ]

    return success_response(
        message=f"Causelist fetched for Judge '{judge}' on {date}.",
        data={
            "inserted_records": inserted,
            "skipped_duplicates": skipped,
            "total_records": len(data),
            "records": data
        },
        status=200
    )
