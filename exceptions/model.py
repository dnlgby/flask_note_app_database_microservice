# Copyright (c) 2023 Daniel Gabay

from exceptions.database_service_exception import DatabaseServiceException


class DatabaseValidationError(DatabaseServiceException):
    def __init__(self, message):
        self.message = message
