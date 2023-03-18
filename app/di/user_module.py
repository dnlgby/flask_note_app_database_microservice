# Copyright (c) 2023 Daniel Gabay

from injector import singleton, Module

from app.data.repositories.user_repository import UserRepository
from app.services.user_service import UserService


class UserModule(Module):
    def configure(self, binder):
        binder.bind(UserRepository, UserRepository, scope=singleton)
        binder.bind(UserService, UserService, scope=singleton)
