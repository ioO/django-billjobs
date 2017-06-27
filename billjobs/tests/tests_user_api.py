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
                'update': {'username': 'bar'}
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
                'GET': self.error_message['401'],
                'POST': {
                    'url': 'http://testserver/billjobs/api/1.0/users/6/',
                    'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.org'
                    },
                'PUT': self.error_message['401'],
                'DELETE': self.error_message['401'],
                'HEAD': self.error_message['401'],
                'OPTIONS': self.error_message['401'],
                'PATCH': self.error_message['401'],
                }

    def tearDown(self):
        super().tearDown()

    def test_user_api_status_code(self):
        self.status_code_is()

    def test_user_api_content(self):
        self.content_is()

class AnonymousUserDetailAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /users/pk endpoint for
    anonymous user.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('users-detail-api', args=(1,))
        self.data = {
                'create': {
                    'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.org'
                    },
                'update': {'username': 'bar'}
                }
        self.expected_status = {
                'GET': 401,
                'POST': 401,
                'PUT': 401,
                'DELETE': 401,
                'HEAD': 401,
                'OPTIONS': 401,
                'PATCH': 401,
                }
        self.expected_content = {
                'GET': self.error_message['401'],
                'POST': self.error_message['401'],
                'PUT': self.error_message['401'],
                'DELETE': self.error_message['401'],
                'HEAD': self.error_message['401'],
                'OPTIONS': self.error_message['401'],
                'PATCH': self.error_message['401'],
                }

    def tearDown(self):
        super().tearDown()

    def test_user_detail_api_status_code(self):
        self.status_code_is()

    def test_user_detail_api_content(self):
        self.content_is()

class UserUserAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /users endpoint for
    authenticated user.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('users-api')
        self.force_authenticate(user=self.bill)
        self.data = {
                'create': {
                    'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.org'
                    },
                'update': {'username': 'bar'}
                }
        self.expected_status = {
                'GET': 200,
                'POST': 201,
                'PUT': 403,
                'DELETE': 403,
                'HEAD': 403,
                'OPTIONS': 403,
                'PATCH': 403,
                }
        self.expected_content = {
                'GET': {
                    'url': 'http://testserver/billjobs/api/1.0/users/3/',
                    'username': 'bill',
                    'email': 'bill@billjobs.org'
                    },
                'POST': {
                    'url': 'http://testserver/billjobs/api/1.0/users/6/',
                    'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.org'
                    },
                'PUT': self.error_message['403'],
                'DELETE': self.error_message['403'],
                'HEAD': self.error_message['403'],
                'OPTIONS': self.error_message['403'],
                'PATCH': self.error_message['403'],
                }

    def tearDown(self):
        super().tearDown()

    def test_user_api_status_code(self):
        self.status_code_is()

    def test_user_api_content(self):
        self.content_is()

class UserUserDetailAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /users/pk endpoint for
    authenticated user.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('users-detail-api', args=(3,))
        self.force_authenticate(user=self.bill)
        self.data = {
                'create': {
                    'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.org'
                    },
                'update': {'username': 'bar'}
                }
        self.expected_status = {
                'GET': 200,
                'POST': 403,
                'PUT': 200,
                'DELETE': 204,
                'HEAD': 403,
                'OPTIONS': 403,
                'PATCH': 403,
                }
        self.expected_content = {
                'GET': {
                    'url': 'http://testserver/billjobs/api/1.0/users/3/',
                    'username': 'bill',
                    'email': 'bill@billjobs.org'
                    },
                'POST': self.error_message['403'],
                'PUT': {
                    'url': 'http://testserver/billjobs/api/1.0/users/3/',
                    'username': 'bar',
                    'email': 'bill@billjobs.org'
                    },
                'DELETE': None,
                'HEAD': self.error_message['403'],
                'OPTIONS': self.error_message['403'],
                'PATCH': self.error_message['403'],
                }

    def tearDown(self):
        super().tearDown()

    def test_user_detail_api_status_code(self):
        self.status_code_is()

    def test_user_detail_api_content(self):
        self.content_is()

    def test_user_can_not_retrieve_other_user(self):
        """
        An authenticated user can not retrieve information of another user
        """
        self.expected_status = { 'GET': 403 }
        self.expected_content = { 'GET': self.error_message['403'] }
        self.url = reverse('users-detail-api', args=(4,))
        self.status_code_is()
        self.content_is()

    def test_user_can_not_update_other_user(self):
        """
        An authenticated user can not update information of another user
        """
        self.expected_status = { 'PUT': 403 }
        self.expected_content = { 'PUT': self.error_message['403'] }
        self.url = reverse('users-detail-api', args=(4,))
        self.status_code_is()
        self.content_is()

    def test_user_can_not_delete_other_user(self):
        """
        An authenticated user can not delete information of another user
        """
        self.expected_status = { 'DELETE': 403 }
        self.expected_content = { 'DELETE': self.error_message['403'] }
        self.url = reverse('users-detail-api', args=(4,))
        self.status_code_is()
        self.content_is()

