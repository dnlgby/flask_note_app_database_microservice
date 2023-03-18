# Copyright (c) 2023 Daniel Gabay

from functools import wraps
from http import HTTPStatus

from flask_smorest import abort

from app.exceptions.model import *
from app.exceptions.repository import *


def view_exception_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except DatabaseValidationError as err:
            abort(HTTPStatus.BAD_REQUEST, message=err.message)
        except ItemNotFoundException as ex:
            abort(HTTPStatus.NOT_FOUND, message=ex.message)
        except ItemAlreadyExistException as ex:
            abort(HTTPStatus.CONFLICT, message=ex.message)
        except PasswordMatchError as ex:
            abort(HTTPStatus.UNAUTHORIZED, message=ex.message)

    return decorated_function
