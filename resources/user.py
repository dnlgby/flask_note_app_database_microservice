# Copyright (c) 2023 Daniel Gabay

from http import HTTPStatus

from flask.views import MethodView
from flask_injector import inject
from flask_smorest import Blueprint

from data.models.user import UserModel
from decorators import view_exception_handler
from schemes import UserSchema
from services.user_service import UserService

blp = Blueprint("users", __name__, description="User operations")


class UserView(MethodView):

    @inject
    def __init__(self, user_service: UserService):
        super().__init__()
        self._user_service = user_service


@blp.route("/user/validate")
class UserValidationView(UserView):

    @blp.arguments(UserSchema)
    @blp.response(HTTPStatus.NO_CONTENT, UserSchema)
    @view_exception_handler
    def post(self, user_data: dict) -> None:
        self._user_service.validate_user(**user_data)


@blp.route("/user")
class UserCreationView(UserView):

    @blp.arguments(UserSchema)
    @blp.response(HTTPStatus.CREATED, UserSchema)
    @view_exception_handler
    def post(self, user_data: dict) -> UserModel:
        return self._user_service.create_user(**user_data)
