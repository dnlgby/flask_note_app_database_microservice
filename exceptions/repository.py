# Copyright (c) 2023 Daniel Gabay

from exceptions.database_service_exception import DatabaseServiceException


class RepositoryException(DatabaseServiceException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"RepositoryException: {self.message}"


class ItemNotFoundException(RepositoryException):
    def __str__(self):
        return f"ItemNotFoundException: {self.message}"


class DatabaseViolationException(RepositoryException):
    def __str__(self):
        return f"DatabaseViolationException: {self.message}"


class ValidationException(RepositoryException):
    def __str__(self):
        return f"ValidationException: {self.message}"
