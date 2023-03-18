#  Copyright (c) 2023 Daniel Gabay

import unittest
from http import HTTPStatus

from flask import json

from app import app


class NoteResourcesTests(unittest.TestCase):

    def setUp(self):
        self._app = app.create_app().test_client()
        self._note_test_payload = {
            'user_id': 1,
            'note_title': "note_title",
            'note_content': "note_content"
        }
        self._note = self.create_note()

    def create_note(self):
        response = self._app.post(
            '/note',
            data=json.dumps(self._note_test_payload),
            content_type='application/json')
        note = json.loads(response.data)
        return note

    def test_note_creation(self):
        response = self._app.post(
            '/note',
            data=json.dumps(self._note_test_payload),
            content_type='application/json')
        data = json.loads(response.data)

        # Assert status code
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        # Assert result format
        self.assertTrue('id' in data and type(data['id']) is int)
        self.assertTrue('note_title' in data and type(data['note_title']) is str)
        self.assertTrue('note_content' in data and type(data['note_content']) is str)

    def test_get_note_list(self):
        response = self._app.get('/note')
        data = json.loads(response.data)

        # Assert result format
        self.assertTrue(type(data) is list)

    def test_get_note_by_id(self):
        response = self._app.get(f'/note/{self._note["id"]}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(data['id'], self._note['id'])
        self.assertEqual(data['note_title'], self._note['note_title'])
        self.assertEqual(data['note_content'], self._note['note_content'])

    def test_patch_note(self):
        updated_data = {
            'note_title': 'Updated Note Title',
            'note_content': 'Updated Note Content'
        }
        response = self._app.patch(
            f'/note/{self._note["id"]}',
            data=json.dumps(updated_data),
            content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(data['id'], self._note['id'])
        self.assertEqual(data['note_title'], updated_data['note_title'])
        self.assertEqual(data['note_content'], updated_data['note_content'])

    def test_delete_note(self):
        note_to_delete = self.create_note()
        response = self._app.delete(
            f'/note/{note_to_delete["id"]}')

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

        # Test if the deleted note is still available
        response = self._app.get(f'/note/{note_to_delete["id"]}')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
