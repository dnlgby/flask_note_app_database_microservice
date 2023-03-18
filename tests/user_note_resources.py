#  Copyright (c) 2023 Daniel Gabay

import random
import string
import unittest
from http import HTTPStatus

from flask import json

from app import app


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


class UserResourcesTests(unittest.TestCase):

    @staticmethod
    def create_random_payload():
        return {
            'username': generate_random_string(8),
            'password': "password"
        }

    def setUp(self):
        self._app = app.create_app().test_client()
        self._user = self.create_user()

    def create_user(self):
        response = self._app.post(
            '/user',
            data=json.dumps(self.create_random_payload()),
            content_type='application/json')
        note = json.loads(response.data)
        return note

    def test_user_creation(self):
        response = self._app.post(
            '/user',
            data=json.dumps(self.create_random_payload()),
            content_type='application/json')
        data = json.loads(response.data)

        # Assert status code
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        # Assert result format
        self.assertTrue('id' in data and type(data['id']) is int)
        self.assertTrue('username' in data and type(data['username']) is str)

    def test_user_validation_success(self):
        created_user = self.create_user()
        response = self._app.post(
            '/user/validate',
            data=json.dumps(
                {
                    'username': created_user['username'],
                    'password': "password"
                }),
            content_type='application/json')

        # Assert status code
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_user_validation_failure(self):
        created_user = self.create_user()
        response = self._app.post(
            '/user/validate',
            data=json.dumps(
                {
                    'username': created_user['username'],
                    'password': "wrong_password"
                }),
            content_type='application/json')

        # Assert status code
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


if __name__ == '__main__':
    unittest.main()
