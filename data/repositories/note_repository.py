#  Copyright (c) 2023 Daniel Gabay

from data.db import database
from data.models.notes import NoteModel
from exceptions.repository import ItemNotFoundException


class NoteRepository:

    @staticmethod
    def create_note(user_id: int, note_title: str, note_content: str) -> NoteModel:
        new_note = NoteModel(user_id=user_id, note_title=note_title, note_content=note_content)
        database.session.add(new_note)
        database.session.commit()
        return new_note

    @staticmethod
    def update_note(note_id: int, note_title: str, note_content: str):
        note = NoteModel.query.get(note_id)
        if note:
            note.note_title = note_title
            note.note_content = note_content
        else:
            raise ItemNotFoundException("Note with the id {note_id} is not found.".format(note_id=note_id))

    @staticmethod
    def delete_note(note_id: int):
        note = NoteModel.query.get(note_id)
        if note:
            database.session.delete(note)
            database.session.commit()
        else:
            raise ItemNotFoundException("Note with the id {note_id} is not found.".format(note_id=note_id))
