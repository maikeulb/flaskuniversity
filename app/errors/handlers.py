from app.extensions import db
from app.errors import errors
from app.api.errors import error_response as api_error_response


@errors.app_errorhandler(404)
def not_found_error(error):
    return api_error_response(404)


@errors.app_errorhandler(401)
def not_found_error(error):
    return api_error_response(401)


@errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return api_error_response(500)
