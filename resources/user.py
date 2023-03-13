#  Copyright (c) 2023 Daniel Gabay

from http import HTTPStatus

from flask.views import MethodView
from flask_injector import inject
from flask_smorest import Blueprint

from data.models.user import UserModel
from decorators import view_exception_handler
from schemes import UserSchema
from services.user_service import UserService

blp = Blueprint("users", __name__, description="User operations")


@blp.route("/user")
class UserView(MethodView):

    @inject
    def __init__(self, user_service: UserService):
        super().__init__()
        self._user_service = user_service

    @blp.arguments(UserSchema)
    @blp.response(HTTPStatus.OK, UserSchema)
    @view_exception_handler
    def get(self, user_data: dict) -> UserModel:
        return self._user_service.get_user(user_data["username"])

    @blp.arguments(UserSchema)
    @blp.response(HTTPStatus.OK, UserSchema)
    @view_exception_handler
    def post(self, user_data: dict) -> UserModel:
        return self._user_service.create_user(**user_data)
