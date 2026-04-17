from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from app.utils import error_response, success_response

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/db/countsalldetails', methods=['GET'])
@jwt_required()
def generate_dash_count(estcode):
    jwt_estcode = get_jwt().get('estcode')
    if jwt_estcode != estcode:
        return error_response(
            'forbidden',
            'Invalid establishment code',
            status=403
        )
    return success_response(
        message=f"Dashboard data fetched for EST '{estcode}'.",
        data=None,
        status=200
    )