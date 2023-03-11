#  Copyright (c) 2023 Daniel Gabay

from flask_jwt_extended import create_access_token
from injector import inject
from passlib.hash import pbkdf2_sha256

from data.repositories.user_repository import UserRepository
from exceptions.repository import ItemNotFoundException
from exceptions.services import InvalidCredentialsException


class UserService:

    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def login(self, username: str, password: str) -> str:
        try:
            user = self._user_repository.get_user_by_name(username)
        except ItemNotFoundException:
            raise InvalidCredentialsException("Invalid Credentials")

        if pbkdf2_sha256.verify(password, user.password):
            access_token = create_access_token(identity=user.id)
            return access_token
        else:
            raise InvalidCredentialsException("Invalid Credentials")
