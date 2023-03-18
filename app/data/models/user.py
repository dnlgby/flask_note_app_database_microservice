# Copyright (c) 2023 Daniel Gabay

from sqlalchemy.orm import validates

from app.data.db import database
from app.data.models.models_constants import ModelsConstants as Consts
from app.exceptions.model import DatabaseValidationError


class UserModel(database.Model):
    __tablename__ = "users"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String(Consts.UserModel.USER_NAME_MAX_LENGTH), unique=True, nullable=False)
    password = database.Column(database.String(Consts.UserModel.PASSWORD_MAX_LENGTH), nullable=False)

    @validates('username')
    def validate_username(self, key, username):
        min_length = 6
        if len(username) < min_length:
            raise DatabaseValidationError(f"username must be at least {min_length} characters long")
        return username
