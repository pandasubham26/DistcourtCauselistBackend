from flask import jsonify
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .utils import error_response


class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None, error_code='api_error'):
        Exception.__init__(self)
        self.message = message
        self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['error'] = self.error_code
        return rv


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        data = error.to_dict()
        return error_response(
            error=data.get('error', 'api_error'),
            message=data.get('message'),
            details={k: v for k, v in data.items() if k not in ['error', 'message']} or None,
            status=getattr(error, 'status_code', 400)
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return error_response('validation_error', 'Validation failed', details=e.messages, status=400)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e: IntegrityError):
        app.logger.exception('Database integrity error')
        return error_response('conflict', 'Resource conflict or constraint violation', status=409)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        # Use e.code and e.description for standardized message
        code = e.code or 500
        error_map = {
            400: 'bad_request',
            401: 'unauthorized',
            403: 'forbidden',
            404: 'not_found',
            405: 'method_not_allowed',
            409: 'conflict',
            422: 'unprocessable_entity',
        }
        err = error_map.get(code, 'http_error')
        return error_response(err, e.description or err.replace('_', ' '), status=code)

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.exception('Unhandled Exception:')
        return error_response('server_error', 'internal server error', status=500)
