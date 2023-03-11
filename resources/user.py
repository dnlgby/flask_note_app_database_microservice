#  Copyright (c) 2023 Daniel Gabay

from flask.views import MethodView
from flask_smorest import Blueprint
from flask_injector import inject

from services.user_service import UserService

blp = Blueprint("Users", __name__, description="User operations")

@blp.route("/register")
class UserRegisterView(MethodView):

    @inject
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def post(self, user_data):
        self._user_service.login(user_data["username"], user_data["password"])
