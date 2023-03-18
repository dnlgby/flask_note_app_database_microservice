# Copyright (c) 2023 Daniel Gabay

from typing import List

from sqlalchemy.exc import IntegrityError

from app.data.db import database
from app.data.models.notes import NoteModel
from app.exceptions.repository import ItemNotFoundException


class NoteRepository:

    @staticmethod
    def get_all_notes() -> List[NoteModel]:
        return NoteModel.query.all()

    @staticmethod
    def get_note_by_id(note_id: int) -> NoteModel:
        note = NoteModel.query.get(note_id)
        if note is None:
            raise ItemNotFoundException("Note with the id {note_id} is not found.".format(note_id=note_id))
        return note

    @staticmethod
    def create_note(user_id: int, note_title: str, note_content: str) -> NoteModel:
        try:
            new_note = NoteModel(user_id=user_id, note_title=note_title, note_content=note_content)
            database.session.add(new_note)
            database.session.commit()
        except IntegrityError:
            database.session.rollback()
            raise ItemNotFoundException("User with the id {user_id} is not found.".format(user_id=user_id))
        return new_note

    @staticmethod
    def update_note(note_id: int, note_title: str, note_content: str) -> NoteModel:
        note = NoteModel.query.get(note_id)
        if note:
            note.note_title = note_title
            note.note_content = note_content
            database.session.add(note)
            database.session.commit()
            return note
        else:
            database.session.rollback()
            raise ItemNotFoundException("Note with the id {note_id} is not found.".format(note_id=note_id))

    @staticmethod
    def delete_note(note_id: int) -> None:
        note = NoteModel.query.get(note_id)
        if note:
            database.session.delete(note)
            database.session.commit()
        else:
            database.session.rollback()
            raise ItemNotFoundException("Note with the id {note_id} is not found.".format(note_id=note_id))
