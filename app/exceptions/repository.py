# Copyright (c) 2023 Daniel Gabay

from app.exceptions.database_service_exception import DatabaseServiceException


class RepositoryException(DatabaseServiceException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"RepositoryException: {self.message}"


class ItemNotFoundException(RepositoryException):
    def __str__(self):
        return f"ItemNotFoundException: {self.message}"


class ItemAlreadyExistException(RepositoryException):
    def __str__(self):
        return f"ItemAlreadyExistException: {self.message}"


class PasswordMatchError(RepositoryException):
    def __str__(self):
        return f"PasswordMatchError: {self.message}"
