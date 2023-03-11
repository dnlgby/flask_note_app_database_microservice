#  Copyright (c) 2023 Daniel Gabay

class ServiceException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"ServiceException: {self.message}"


class InvalidCredentialsException(ServiceException):
    def __str__(self):
        return f"InvalidCredentialsException: {self.message}"
