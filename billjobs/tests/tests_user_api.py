from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from billjobs.tests.generics import GenericAPITest, GenericAPIStatusCode
import collections

class AnonymousUserAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /users endpoint for
    anonymous user.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('users-api')
        self.data = {
                'create': {
                    'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.org'
                    },
                'update': {'name': 'new name'}
                }
        self.expected_status = {
                'GET': 401,
                'POST': 201,
                'PUT': 401,
                'DELETE': 401,
                'HEAD': 401,
                'OPTIONS': 401,
                'PATCH': 401,
                }
        self.expected_content = {
                'GET': {
                    'detail': 'Authentication credentials were not provided.'},
                'POST': {
                    'url': 'http://testserver/billjobs/api/1.0/users/6/',
                    'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.org'
                    },
                'PUT': {
                    'detail': 'Authentication credentials were not provided.'},
                'DELETE': {
                    'detail': 'Authentication credentials were not provided.'},
                'HEAD': {
                    'detail': 'Authentication credentials were not provided.'},
                'OPTIONS': {
                    'detail': 'Authentication credentials were not provided.'},
                'PATCH': {
                    'detail': 'Authentication credentials were not provided.'},
                }

    def tearDown(self):
        super().tearDown()

    def test_group_api_status_code(self):
        self.status_code_is()

    def test_group_api_content(self):
        self.content_is()

    def test_user_detail_put_return_error_when_duplicate_username(self):
        """
        Test api user detail endpoint with PUT method return an error when
        an username already exists
        information
        """
        data = {'username': 'bill'}
        json_data = super().get_json('PUT', self.url, data)
        self.assertIn('A user with that username already exists.',
                json_data['username'])

