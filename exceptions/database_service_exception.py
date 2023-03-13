# Copyright (c) 2023 Daniel Gabay

class DatabaseServiceException(Exception):
    def __init__(self, message):
        self.message = message
