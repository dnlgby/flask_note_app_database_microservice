#  Copyright (c) 2023 Daniel Gabay

from sqlalchemy.exc import IntegrityError

from data.db import database
from data.models.user import UserModel
from exceptions.repository import ItemNotFoundException, DatabaseViolationException


class UserRepository:

    @staticmethod
    def create_user(username: str, password: str) -> UserModel:
        try:
            new_user = UserModel(username=username, password=password)
            database.session.add(new_user)
            database.session.commit()
        except IntegrityError:
            raise DatabaseViolationException("User with that name is already exist.")
        return new_user

    @staticmethod
    def get_user_by_name(username: str) -> UserModel:
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            raise ItemNotFoundException("User with the name {username} is not found.".format(username=username))
        return user
