#  Copyright (c) 2023 Daniel Gabay

from injector import Module, singleton

from data.repositories.user_repository import UserRepository
from services.user_service import UserService


class UserRepositoryModule(Module):
    def configure(self, binder):
        binder.bind(UserRepository, to=UserRepository(), scope=singleton)


class UserServiceModule(Module):
    def configure(self, binder):
        binder.bind(UserService, to=UserService(singleton(UserRepository)))
