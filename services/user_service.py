# Copyright (c) 2023 Daniel Gabay

from injector import inject

from data.models.user import UserModel
from data.repositories.user_repository import UserRepository


class UserService:

    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def validate_user(self, username: str, password: str) -> None:
        return self._user_repository.validate_user(username=username, password=password)

    def create_user(self, username: str, password: str) -> UserModel:
        return self._user_repository.create_user(username=username, password=password)
