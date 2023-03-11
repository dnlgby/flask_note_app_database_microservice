#  Copyright (c) 2023 Daniel Gabay


class RepositoryException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"RepositoryError: {self.message}"


class ItemNotFoundException(RepositoryException):
    def __str__(self):
        return f"ItemNotFoundException: {self.message}"