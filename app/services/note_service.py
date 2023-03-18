# Copyright (c) 2023 Daniel Gabay

from typing import List

from injector import inject

from app.data.models.notes import NoteModel
from app.data.repositories.note_repository import NoteRepository


class NoteService:

    @inject
    def __init__(self, note_repository: NoteRepository):
        self._note_repository = note_repository

    def get_all_notes(self) -> List[NoteModel]:
        return self._note_repository.get_all_notes()

    def get_note(self, note_id: int) -> NoteModel:
        return self._note_repository.get_note_by_id(note_id=note_id)

    def create_note(self, user_id: int, note_title: str, note_content: str) -> NoteModel:
        return self._note_repository.create_note(
            user_id=user_id, note_title=note_title, note_content=note_content)

    def update_note(self, note_id: int, note_title: str, note_content: str) -> NoteModel:
        return self._note_repository.update_note(
            note_id=note_id, note_title=note_title, note_content=note_content)

    def delete_note(self, note_id: int) -> None:
        self._note_repository.delete_note(note_id)
