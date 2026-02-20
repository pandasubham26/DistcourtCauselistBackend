
from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_
from app.estcode_db import get_cis_db_key
from app.extensions import db
from app.models.cis.registry import get_cis_model
from app.models.master.user import User
from app.schemas.case_type_schema import casetype_schema
from app.schemas.court_schema import court_schema
from app.schemas.designation_schema import designation_schema
from app.schemas.state_schema import state_schema
from app.schemas.user_schema import user_schema, ALLOWED_ROLES
from app.utils import error_response, success_response

master_bp = Blueprint('master_bp', __name__)


@master_bp.route('/ct/getcasetype', methods=['GET'])
@jwt_required()
def get_casetype(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        db_key = get_cis_db_key(estcode)
        CaseTypeT = get_cis_model(db_key, 'case_type_t')

        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        search = (request.args.get('search') or '').strip().lower()
        sort_key = request.args.get('sort_key', 'name').strip().lower()
        sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

        if page < 1:
            return error_response('validation_error', 'Page must be at least 1', status=400)
        if page_size < 1 or page_size > 100:
            return error_response('validation_error', 'Page size must be between 1 and 100', status=400)

        allowed_sort_keys = {'id', 'username', 'email', 'role', 'created_at'}
        if sort_key not in allowed_sort_keys:
            sort_key = 'username'

        # Fetch all users
        query = CaseTypeT.query.filter(CaseTypeT.display == 'Y')

        if search:
            query = query.filter(
                db.or_(
                    db.func.lower(CaseTypeT.type_name).contains(search)
                )
            )

        sort_column = getattr(CaseTypeT, sort_key, CaseTypeT.type_name)
        if sort_dir == 'desc':
            sort_column = sort_column.desc()

        query = query.order_by(sort_column)

        total = query.count()
        casetype = query.offset((page - 1) * page_size).limit(page_size).all()

        # If no users found
        if not casetype:
            return error_response(
                details={
                    'casetype': [],
                    'paginations': {
                        'total': 0,
                        'page': page,
                        'page_size': page_size,
                        'pages': 0
                    }
                },
                error='no_users',
                message='No case type found',
                status=404
            )

        case_type_list = casetype_schema.dump(casetype, many=True)
        # Serialize with schema (many=True for lists)
        return success_response(
            data={
                'casetype': case_type_list,
                'paginations': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'pages': (total + page_size - 1)
                }
            },
            message='case type fetched successfully',
            status=200
        )

    except Exception:
        current_app.logger.exception('Error fetching user list')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@master_bp.route('/cn/getcourtname', methods=['GET'])
@jwt_required()
def get_court(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        db_key = get_cis_db_key(estcode)
        CourtName = get_cis_model(db_key, 'court_name')
        
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        search = (request.args.get('search') or '').strip().lower()
        sort_key = request.args.get('sort_key', 'state').strip().lower()
        sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

        if page < 1:
            return error_response('validation_error', 'Page must be at least 1', status=400)
        if page_size < 1 or page_size > 100:
            return error_response('validation_error', 'Page size must be between 1 and 100', status=400)

        allowed_sort_keys = {'state'}
        if sort_key not in allowed_sort_keys:
            sort_key = 'state'

        # Fetch all users
        query = CourtName.query

        if search:
            query = query.filter(
                db.or_(
                    db.func.lower(CourtName.state).contains(search)
                )
            )

        sort_column = getattr(CourtName, sort_key, CourtName.state)
        if sort_dir == 'desc':
            sort_column = sort_column.desc()

        query = query.order_by(sort_column)

        total = query.count()
        state = query.offset((page - 1) * page_size).limit(page_size).all()

        # If no users found
        if not state:
            return error_response(
                details={
                    'court': [],
                    'paginations': {
                        'total': 0,
                        'page': page,
                        'page_size': page_size,
                        'pages': 0
                    }
                },
                error='no_court',
                message='No court found',
                status=404
            )

        court_list = court_schema.dump(state, many=True)
        # Serialize with schema (many=True for lists)
        return success_response(
            data={
                'court': court_list,
                'paginations': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'pages': ((total + page_size - 1) // page_size)
                }
            },
            message='court fetched successfully',
            status=200
        )

    except Exception:
        current_app.logger.exception('Error fetching court list')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@master_bp.route('/dg/getdesignation', methods=['GET'])
@jwt_required()
def get_designation(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        db_key = get_cis_db_key(estcode)
        DesignationName = get_cis_model(db_key, 'desg_t')

        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        search = (request.args.get('search') or '').strip().lower()
        sort_key = request.args.get('sort_key', 'state').strip().lower()
        sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

        if page < 1:
            return error_response('validation_error', 'Page must be at least 1', status=400)
        if page_size < 1 or page_size > 100:
            return error_response('validation_error', 'Page size must be between 1 and 100', status=400)

        allowed_sort_keys = {'state'}
        if sort_key not in allowed_sort_keys:
            sort_key = 'state'

        # Fetch all users
        query = DesignationName.query

        if search:
            query = query.filter(
                db.or_(
                    db.func.lower(DesignationName.desgname).contains(search)
                )
            )

        sort_column = getattr(DesignationName, sort_key, DesignationName.desgname)
        if sort_dir == 'desc':
            sort_column = sort_column.desc()

        query = query.order_by(sort_column)

        total = query.count()
        designation = query.offset((page - 1) * page_size).limit(page_size).all()

        # If no users found
        if not designation:
            return error_response(
                details={
                    'designation': [],
                    'paginations': {
                        'total': 0,
                        'page': page,
                        'page_size': page_size,
                        'pages': 0
                    }
                },
                error='no_designation',
                message='No designation found',
                status=404
            )

        designation_list = designation_schema.dump(designation, many=True)
        # Serialize with schema (many=True for lists)
        return success_response(
            data={
                'designation': designation_list,
                'paginations': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'pages': ((total + page_size - 1) // page_size)
                }
            },
            message='designation fetched successfully',
            status=200
        )

    except Exception:
        current_app.logger.exception('Error fetching designation list')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@master_bp.route('/dt/getdistrict', methods=['GET'])
@jwt_required()
def get_dist(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        db_key = get_cis_db_key(estcode)
        MainState = get_cis_model(db_key, 'state')
        District = get_cis_model(db_key, 'district_t')

        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        search = (request.args.get('search') or '').strip().lower()
        sort_key = request.args.get('sort_key', 'state').strip().lower()
        sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

        if page < 1:
            return error_response('validation_error', 'Page must be at least 1', status=400)
        if page_size < 1 or page_size > 100:
            return error_response('validation_error', 'Page size must be between 1 and 100', status=400)

        allowed_sort_keys = {'state', 'dist_name'}
        if sort_key not in allowed_sort_keys:
            sort_key = 'state'

        # Fetch all districts with their state name
        query = db.session.query(District, MainState.state).select_from(District).join(
            MainState,
            District.state_id == MainState.state_id
        ).filter(District.display == 'Y')

        if search:
            query = query.filter(
                db.or_(
                    db.func.lower(MainState.state).contains(search),
                    db.func.lower(District.dist_name).contains(search)
                )
            )

        if sort_key == 'state':
            sort_column = MainState.state
        else:
            sort_column = District.dist_name

        if sort_dir == 'desc':
            sort_column = sort_column.desc()

        query = query.order_by(sort_column)

        total = query.count()
        district = query.offset((page - 1) * page_size).limit(page_size).all()

        # If no districts found
        if not district:
            return error_response(
                details={
                    'district': [],
                    'paginations': {
                        'total': 0,
                        'page': page,
                        'page_size': page_size,
                        'pages': 0
                    }
                },
                error='no_district',
                message='No district found',
                status=404
            )

        # dist_list = district_schema.dump(district, many=True)
        district_list = [
            {
                'state_name': state_name,
                'district_name': district.dist_name,
                'dist_id': district.dist_code,
                'state_id': district.state_id,
                'display': district.display,
                'create_modify': district.create_modify
            }
            for district, state_name in district
        ]
        # Serialize with schema (many=True for lists)
        return success_response(
            data={
                'district': district_list,
                'paginations': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'pages': ((total + page_size - 1) // page_size)
                }
            },
            message='States and districts fetched successfully',
            status=200
        )

    except Exception:
        current_app.logger.exception('Error fetching state and district list')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@master_bp.route('/jd/getjudges', methods=['GET'])
@jwt_required()
def get_judge(estcode):
    try:
        # 🔐 Validate estcode with JWT
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        # Resolve DB + models
        db_key = get_cis_db_key(estcode)
        JudgeName = get_cis_model(db_key, 'judge_name_t')
        Designation = get_cis_model(db_key, 'desg_t')
        JudgeWithCourt = get_cis_model(db_key, 'judge_t')

        # Pagination & filters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        search = (request.args.get('search') or '').strip().lower()
        sort_key = request.args.get('sort_key', 'judge_name').lower()
        sort_dir = request.args.get('sort_dir', 'asc').lower()

        if page < 1:
            return error_response('validation_error', 'Page must be >= 1', 400)
        if not 1 <= page_size <= 100:
            return error_response('validation_error', 'Page size must be 1–100', 400)

        allowed_sort_keys = {'judge_name', 'desgname', 'jocode'}
        if sort_key not in allowed_sort_keys:
            sort_key = 'judge_name'

        # ✅ BASE QUERY (IMPORTANT)
        query = (
            db.session.query(JudgeName, Designation)
            .join(Designation, JudgeName.desg_code == Designation.desgcode)
            .join(JudgeWithCourt, JudgeName.jocode == JudgeWithCourt.jocode)
            .filter(
                and_(
                    JudgeWithCourt.display == 'Y',
                    JudgeWithCourt.from_dt.isnot(None),
                    JudgeWithCourt.to_dt.is_(None)
                )
            )
        )

        # 🔍 Search
        if search:
            query = query.filter(
                or_(
                    db.func.lower(JudgeName.judge_name).contains(search),
                    db.func.lower(Designation.desgname).contains(search),
                    db.func.lower(JudgeName.jocode).contains(search)
                )
            )

        # 🔃 Sorting
        if sort_key == 'judge_name':
            sort_column = JudgeName.judge_name
        elif sort_key == 'desgname':
            sort_column = Designation.desgname
        else:
            sort_column = JudgeName.jocode

        if sort_dir == 'desc':
            sort_column = sort_column.desc()

        query = query.order_by(sort_column)

        # 📊 Count BEFORE pagination
        total = query.count()

        # 📄 Pagination
        rows = (
            query
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        if not rows:
            return success_response(
                data={
                    'judge': [],
                    'paginations': {
                        'total': total,
                        'page': page,
                        'page_size': page_size,
                        'pages': 0
                    }
                },
                message='No judge found',
                status=200
            )

        # 🧾 Serialize
        judge_list = [
            {
                'judge_code': judge.judge_code,
                'judge_name': judge.judge_name,
                'desg_code': judge.desg_code,
                'desgname': desg.desgname,
                'jocode': judge.jocode,
                'est_code_src': judge.est_code_src,
                'display': judge.display
            }
            for judge, desg in rows
        ]

        return success_response(
            data={
                'judge': judge_list,
                'paginations': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'pages': (total + page_size - 1) // page_size
                }
            },
            message='Judge and designation fetched successfully',
            status=200
        )

    except Exception:
        current_app.logger.exception(
            f'Error fetching judge list for estcode={estcode}'
        )
        return error_response(
            'server_error',
            'An unexpected error occurred',
            status=500
        )


@master_bp.route('/st/getstate', methods=['GET'])
@jwt_required()
def get_state(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        db_key = get_cis_db_key(estcode)
        MainState = get_cis_model(db_key, 'state')

        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        search = (request.args.get('search') or '').strip().lower()
        sort_key = request.args.get('sort_key', 'state').strip().lower()
        sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

        if page < 1:
            return error_response('validation_error', 'Page must be at least 1', status=400)
        if page_size < 1 or page_size > 100:
            return error_response('validation_error', 'Page size must be between 1 and 100', status=400)

        allowed_sort_keys = {'state'}
        if sort_key not in allowed_sort_keys:
            sort_key = 'state'

        # Fetch all users
        query = MainState.query

        if search:
            query = query.filter(
                db.or_(
                    db.func.lower(MainState.state).contains(search)
                )
            )

        sort_column = getattr(MainState, sort_key, MainState.state)
        if sort_dir == 'desc':
            sort_column = sort_column.desc()

        query = query.order_by(sort_column)

        total = query.count()
        state = query.offset((page - 1) * page_size).limit(page_size).all()

        # If no state found
        if not state:
            return error_response(
                details={
                    'state': [],
                    'paginations': {
                        'total': 0,
                        'page': page,
                        'page_size': page_size,
                        'pages': 0
                    }
                },
                error='no_states',
                message='No state found',
                status=404
            )

        state_list = state_schema.dump(state, many=True)
        # Serialize with schema (many=True for lists)
        return success_response(
            data={
                'state': state_list,
                'paginations': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'pages': ((total + page_size - 1) // page_size)
                }
            },
            message='state fetched successfully',
            status=200
        )

    except Exception:
        current_app.logger.exception('Error fetching state list')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@master_bp.route('/us/getusers', methods=['GET'])
@jwt_required()
def get_users(estcode):
    try:
        jwt_estcode = get_jwt().get('estcode')
        if jwt_estcode != estcode:
            return error_response(
                'forbidden',
                'Invalid establishment code',
                status=403
            )

        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)
        search = (request.args.get('search') or '').strip().lower()
        sort_key = request.args.get('sort_key', 'username').strip().lower()
        sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

        if page < 1:
            return error_response('validation_error', 'Page must be at least 1', status=400)
        if page_size < 1 or page_size > 100:
            return error_response('validation_error', 'Page size must be between 1 and 100', status=400)

        allowed_sort_keys = {'id', 'username', 'email', 'role', 'created_at'}
        if sort_key not in allowed_sort_keys:
            sort_key = 'username'

        sort_column = getattr(User, sort_key, User.username)
        if sort_dir == 'desc':
            sort_column = sort_column.desc()

        # Fetch all users
        query = User.query.filter(User.estcode == estcode)

        if search:
            query = query.filter(
                db.or_(
                    db.func.lower(User.username).contains(search),
                    db.func.lower(User.email).contains(search),
                    db.func.lower(User.role).contains(search)
                )
            )

        query = query.order_by(sort_column)

        total = query.count()
        users = query.offset((page - 1) * page_size).limit(page_size).all()

        # If no users found
        if not users:
            return error_response(
                details={
                    'users': [],
                    'paginations': {
                        'total': 0,
                        'page': page,
                        'page_size': page_size,
                        'pages': 0
                    }
                },
                error='no_users',
                message='No users found',
                status=404
            )

        user_list = user_schema.dump(users, many=True)
        # Serialize with schema (many=True for lists)
        return success_response(
            data={
                'users': user_list,
                'paginations': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'pages': ((total + page_size - 1) // page_size)
                }
            },
            message='User list fetched successfully',
            status=200
        )

    except Exception:
        current_app.logger.exception('Error fetching user list')
        return error_response('server_error', 'An unexpected error occurred', status=500)


@master_bp.route('/us/adduser', methods=['POST'])
@jwt_required()
def create_user(estcode):
    jwt_estcode = get_jwt().get('estcode')
    if jwt_estcode != estcode:
        return error_response(
            'forbidden',
            'Invalid establishment code',
            status=403
        )

    json_data = request.get_json() or {}
    if 'payload' in json_data:
        json_data = json_data.get('payload', {})

    # validation using schema
    errors = user_schema.validate(json_data)
    if errors:
        return error_response('validation_error', 'Validation failed', details=errors, status=400)

    # Normalize and validate role
    role = (json_data.get('role') or '').lower()
    if role not in ALLOWED_ROLES:
        return error_response('validation_error', 'Invalid role', details={'role': [f"Role must be one of: {', '.join(ALLOWED_ROLES)}"]}, status=400)

    # create user object
    user = User(
        username=json_data['username'],
        email=json_data['email'],
        estcode=estcode,
        judge=json_data.get('judge'),
        role=role,
    )

    # set password securely
    password_hash = json_data.get('password')
    if not password_hash:
        return error_response('validation_error', 'Password is required', details={'password': ['Missing password']}, status=400)
    user.set_password(password_hash)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        current_app.logger.exception('Integrity error while creating user')
        return error_response('conflict', 'username or email already exists', status=409)
    except Exception:
        db.session.rollback()
        current_app.logger.exception('Unexpected error while creating user')
        return error_response('server_error', 'an unexpected error occurred', status=500)


@master_bp.route('/us/updatestatus/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_status(estcode, user_id):
    jwt_estcode = get_jwt().get('estcode')
    if jwt_estcode != estcode:
        return error_response(
            'forbidden',
            'Invalid establishment code',
            status=403
        )

    json_data = request.get_json() or {}

    # validation using schema
    if 'isactive' not in json_data:
        return error_response(
            'validation_error',
            'isactive field is required',
            details={'isactive': ['Missing isactive']},
            status=400
        )

    isactive = json_data.get('isactive')
    if not isinstance(isactive, bool):
        return error_response(
            'validation_error',
            'isactive must be boolean',
            details={'isactive': ['Must be true or false']},
            status=400
        )

    user = User.query.filter_by(
        id=user_id,
        estcode=jwt_estcode
    ).first()

    if not user:
        return error_response(
            'not_found',
            'User not found',
            status=404
        )

    user.isactive = isactive

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.exception('Error updating user status')
        return error_response(
            'server_error',
            'Failed to update user status',
            status=500
        )

    return success_response(
        'success',
        'User status updated successfully',
        200
    )

    