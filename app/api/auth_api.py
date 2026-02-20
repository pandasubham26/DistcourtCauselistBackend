from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.schemas.user_schema import user_schema, ALLOWED_ROLES
from app.utils import success_response, error_response
from app.models.master.user import User

authentication_bp = Blueprint('authentication_bp', __name__)


@authentication_bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json() or {}

    # Validate input
    office_code = json_data.get('officeCode')
    username_or_email = json_data.get('username') or json_data.get('email')
    password = json_data.get('password')

    if not office_code or not username_or_email or not password:
        return error_response(
            'validation_error',
            'Office code, username/email and password are required',
            status=400
        )

    # Fetch user by username or email
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if not user or not user.check_password(password):
        return error_response('invalid_credentials', 'Invalid username/email or password', status=401)

    if not user.isactive:
        return error_response('inactive', 'User account is inactive', status=403)

    office_mapping = (
        User.query
        .filter_by(id=user.id, estcode=office_code, isactive=True)
        .first()
    )

    if not office_mapping:
        return error_response(
            'invalid_office',
            'User does not have access to this office',
            status=403
        )

    # Create JWT tokens
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            'estcode': office_code,
            'role': user.role
        }
    )
    try:
        from flask_jwt_extended import create_refresh_token
        refresh_token = create_refresh_token(identity=str(user.id),
                                             additional_claims={
                                                 'estcode': office_code,
                                                 'role': user.role
                                             }
                                             )
    except Exception:
        refresh_token = None

    payload = {'access_token': access_token, 'user': user.to_dict(), 'estcode': office_code}

    if refresh_token:
        payload['refresh_token'] = refresh_token

    return success_response(
        data=payload,
        message='Login successful',
        status=200
    )


@authentication_bp.route('/register', methods=['POST'])
def create_user():
    json_data = request.get_json() or {}

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

    # use schema to jsonify user as data
    return success_response(data=user_schema.dump(user), message='User created', status=200)