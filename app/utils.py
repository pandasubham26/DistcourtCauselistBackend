from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.master.user import User

# Role to group mapping and group hierarchy
# Supports legacy roles and new requested roles
ROLE_TO_GROUP = {
    # New roles
    'app_admin': 'admin',
    'district_judge': 'readandwrite',
    'judge': 'readandwrite',
    'user': 'readonly',
    # Legacy roles (kept for backward compatibility)
    'admin': 'admin',
    'advocate': 'readonly',
}

GROUP_RANK = {
    'readonly': 1,
    'readandwrite': 2,
    'admin': 3,
}



def success_response(data=None, message=None, status=200):
    payload = {
        'success': True,
        'message': message,
        'data': data,
    }
    # remove None keys to keep responses clean
    payload = {k: v for k, v in payload.items() if v is not None}
    return jsonify(payload), status


def error_response(error, message=None, details=None, status=400):
    payload = {
        'success': False,
        'error': error,
        'message': message,
        'details': details,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    return jsonify(payload), status


def resolve_group_from_role(role: str) -> str:
    if not role:
        return 'readonly'
    return ROLE_TO_GROUP.get(role.lower(), 'readonly')


def log_action(actor_user_id: int, action: str, entity: str = None, entity_id: str = None, details: dict = None):
    """
    Store an audit log entry. Safe to call; will swallow exceptions to avoid breaking main flow.
    """
    try:
        from app.models.audit_log import AuditLog
        entry = AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            entity=entity,
            entity_id=str(entity_id) if entity_id is not None else None,
            details=details or {}
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        # never break main flow due to logging issues
        db.session.rollback()
    return True


def require_group(min_group: str = None, allowed_groups=None):
    """
    Decorator to require a minimum group (hierarchical) or a set of allowed groups.
    - min_group: 'readonly' | 'readandwrite' | 'admin'
    - allowed_groups: iterable of allowed group names

    Note: expects JWT identity to be user id. Returns 401 if not authenticated and 403 if insufficient group.
    """
    if allowed_groups is not None:
        allowed_groups = {g.lower() for g in allowed_groups}

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                user_id = get_jwt_identity()
            except Exception:
                return error_response('unauthorized', 'Missing or invalid authentication', status=401)
            if not user_id:
                return error_response('unauthorized', 'Authentication required', status=401)

            user = db.session.get(User, user_id)
            if not user or not user.isactive:
                return error_response('unauthorized', 'Invalid or inactive user', status=401)

            user_group = user.group

            if allowed_groups is not None:
                if user_group not in allowed_groups:
                    return error_response('forbidden', 'Insufficient permissions', status=403)
            elif min_group is not None:
                if GROUP_RANK.get(user_group, 0) < GROUP_RANK.get(min_group, 0):
                    return error_response('forbidden', 'Insufficient permissions', status=403)

            return fn(*args, **kwargs)
        return wrapper
    return decorator
