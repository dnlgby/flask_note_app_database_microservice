#  Copyright (c) 2023 Daniel Gabay

from data.db import database
from data.models.user import UserModel
from exceptions.repository import ItemNotFoundException


class UserRepository:

    @staticmethod
    def create_user(username: str, password: str) -> UserModel:
        new_user = UserModel(username=username, password=password)
        database.session.add(new_user)
        database.session.commit()
        return new_user

    @staticmethod
    def get_user_by_name(username: str) -> UserModel:
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            raise ItemNotFoundException("User with the name {username} is not found.".format(username=username))
        return user
