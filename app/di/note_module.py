# Copyright (c) 2023 Daniel Gabay

from injector import singleton, Module

from app.data.repositories.note_repository import NoteRepository
from app.services.note_service import NoteService


class NoteModule(Module):
    def configure(self, binder):
        binder.bind(NoteRepository, NoteRepository, scope=singleton)
        binder.bind(NoteService, NoteService, scope=singleton)
