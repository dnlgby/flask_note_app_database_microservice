#  Copyright (c) 2023 Daniel Gabay

from functools import wraps
from http import HTTPStatus

from flask_smorest import abort

from exceptions.repository import *


def view_exception_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ItemNotFoundException as ex:
            abort(HTTPStatus.NOT_FOUND, message=str(ex))
        except DatabaseViolationException as ex:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex))
        except ValidationException as ex:
            abort(HTTPStatus.UNAUTHORIZED, message=str(ex))

    return decorated_function
