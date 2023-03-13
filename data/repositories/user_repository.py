#  Copyright (c) 2023 Daniel Gabay

from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from data.db import database
from data.models.user import UserModel
from exceptions.repository import ItemNotFoundException, DatabaseViolationException, ValidationException


class UserRepository:

    @staticmethod
    def create_user(username: str, password: str) -> UserModel:
        try:
            hashed_password = pbkdf2_sha256.hash(password)
            new_user = UserModel(username=username, password=hashed_password)
            database.session.add(new_user)
            database.session.commit()
        except IntegrityError:
            raise DatabaseViolationException("User with that name is already exist.")
        return new_user

    @staticmethod
    def validate_user(username: str, password: str) -> None:
        hashed_password = pbkdf2_sha256.hash(password)
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            raise ItemNotFoundException("User with the name {username} is not found.".format(username=username))
        if user.password != hashed_password:
            raise ValidationException("Incorrect password for user {username}".format(username=username))
