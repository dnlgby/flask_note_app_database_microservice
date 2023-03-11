#  Copyright (c) 2023 Daniel Gabay

from injector import inject

from data.models.notes import NoteModel
from data.repositories.note_repository import NoteRepository


class NoteService:

    @inject
    def __init__(self, note_repository: NoteRepository):
        self._note_repository = note_repository

    def create_note(self, user_id: int, note_title: str, note_content: str) -> NoteModel:
        return self._note_repository.create_note(
            user_id=user_id, note_title=note_title, note_content=note_content)
