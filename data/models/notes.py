#  Copyright (c) 2023 Daniel Gabay

from data.db import database
from data.models.models_constants import ModelsConstants as Consts


class NoteModel(database.Model):
    __tablename__ = "notes"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    user_id = database.Column(database.Integer, database.ForeignKey("users.id"), nullable=False)
    note_title = database.Column(database.String(Consts.NoteModel.NOTE_TITLE_MAX_LENGTH), nullable=False)
    note_content = database.Column(database.String(Consts.NoteModel.NOTE_CONTENT_MAX_LENGTH), nullable=False)
