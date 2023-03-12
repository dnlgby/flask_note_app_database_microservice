#  Copyright (c) 2023 Daniel Gabay

from exceptions.database_service_exception import DatabaseServiceException


class ServiceException(DatabaseServiceException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"ServiceException: {self.message}"
