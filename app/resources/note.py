# Copyright (c) 2023 Daniel Gabay

from http import HTTPStatus
from typing import List

from flask.views import MethodView
from flask_injector import inject
from flask_smorest import Blueprint

from app.data.models.notes import NoteModel
from app.data.models.user import UserModel
from app.decorators import view_exception_handler
from app.schemes import NoteSchema, NoteUpdateSchema
from app.services.note_service import NoteService

blp = Blueprint("notes", __name__, description="Notes operations")


class NoteView(MethodView):
    @inject
    def __init__(self, note_service: NoteService):
        super().__init__()
        self._note_service = note_service


@blp.route("/note/<int:note_id>")
class NoteItemView(NoteView):

    @blp.response(HTTPStatus.OK, NoteSchema)
    @view_exception_handler
    def get(self, note_id: int) -> UserModel:
        return self._note_service.get_note(note_id=note_id)

    @blp.arguments(NoteUpdateSchema)
    @blp.response(HTTPStatus.OK, NoteSchema)
    @view_exception_handler
    def patch(self, note_data: dict, note_id: int) -> UserModel:
        return self._note_service.update_note(note_id=note_id, **note_data)

    @blp.response(HTTPStatus.NO_CONTENT)
    @view_exception_handler
    def delete(self, note_id: int) -> None:
        self._note_service.delete_note(note_id=note_id)


@blp.route("/note")
class NoteListView(NoteView):

    @blp.arguments(NoteSchema)
    @blp.response(HTTPStatus.CREATED, NoteSchema)
    @view_exception_handler
    def post(self, note_data: dict) -> UserModel:
        return self._note_service.create_note(**note_data)

    @blp.response(HTTPStatus.OK, NoteSchema(many=True))
    def get(self) -> List[NoteModel]:
        return self._note_service.get_all_notes()
