# Copyright (c) 2023 Daniel Gabay

from marshmallow import Schema, fields


class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    note_title = fields.String(required=True)
    note_content = fields.String(required=True)


class NoteUpdateSchema(Schema):
    note_title = fields.String(required=True)
    note_content = fields.String(required=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(load_only=True, required=True)
