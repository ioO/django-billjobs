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
                'HEAD': 401,
                'OPTIONS': 401,
                'PATCH': 401,
                'DELETE': 401,
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
                'HEAD': self.error_message['401'],
                'OPTIONS': self.error_message['401'],
                'PATCH': self.error_message['401'],
                'DELETE': self.error_message['401'],
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
                'HEAD': 401,
                'OPTIONS': 401,
                'PATCH': 401,
                'DELETE': 401,
                }
        self.expected_content = {
                'GET': self.error_message['401'],
                'POST': self.error_message['401'],
                'PUT': self.error_message['401'],
                'HEAD': self.error_message['401'],
                'OPTIONS': self.error_message['401'],
                'PATCH': self.error_message['401'],
                'DELETE': self.error_message['401'],
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
                'HEAD': 403,
                'OPTIONS': 403,
                'PATCH': 403,
                'DELETE': 403,
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
                'HEAD': self.error_message['403'],
                'OPTIONS': self.error_message['403'],
                'PATCH': self.error_message['403'],
                'DELETE': self.error_message['403'],
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
                'HEAD': 403,
                'OPTIONS': 403,
                'PATCH': 403,
                'DELETE': 204,
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
                'HEAD': self.error_message['403'],
                'OPTIONS': self.error_message['403'],
                'PATCH': self.error_message['403'],
                'DELETE': None,
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

class AdminUserAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /users endpoint for
    admin.
    """

    def setUp(self):
        self.maxDiff = None
        super().setUp()
        self.url = reverse('users-api')
        self.force_authenticate(user=self.admin)
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
                'PUT': 405,
                'HEAD': 200,
                'OPTIONS': 200,
                'PATCH': 405,
                'DELETE': 405,
                }
        self.expected_length = {
                'GET': 5,
                'POST': 1
                }
        self.expected_content = {
                'GET': [
                    collections.OrderedDict({
                        'url': 'http://testserver/billjobs/api/1.0/users/1/',
                        'username': 'superuser',
                        'email': 'superuser@billjobs.org',
                        'password': 'pbkdf2_sha256$30000$J1xYbnHgWv7g$LcXs7lgyFtmoDKUn0vzi15jWsLCSDgr6ikOj2/1uNl4=',
                        'is_staff': True,
                        'is_superuser': True,
                        'groups': []
                        }),
                    collections.OrderedDict({
                        'url': 'http://testserver/billjobs/api/1.0/users/2/',
                        'username': 'admin',
                        'email': 'admin@billjobs.org',
                        'is_staff': True,
                        'is_superuser': False,
                        'groups': ['http://testserver/billjobs/api/1.0/groups/1/']
                        }),
                    collections.OrderedDict({
                        'url': 'http://testserver/billjobs/api/1.0/users/3/',
                        'username': 'bill',
                        'email': 'bill@billjobs.org',
                        'is_staff': False,
                        'is_superuser': False,
                        'groups': [
                            'http://testserver/billjobs/api/1.0/groups/2/',
                            'http://testserver/billjobs/api/1.0/groups/3/'
                            ]
                        }),
                    collections.OrderedDict({
                        'url': 'http://testserver/billjobs/api/1.0/users/4/',
                        'username': 'steve',
                        'email': 'steve@billjobs.org',
                        'is_staff': False,
                        'is_superuser': False,
                        }),
                    collections.OrderedDict({
                        'url': 'http://testserver/billjobs/api/1.0/users/5/',
                        'groups': [],
                        'is_superuser': False,
                        'username': 'no-group',
                        'email': 'no-group@billjobs.org',
                        'is_staff': False,
                        'is_active': True,
                        }),
                    ],
                'POST': {
                    'url': 'http://testserver/billjobs/api/1.0/users/6/',
                    'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.org',
                    'groups': [],
                    'is_staff': False,
                    'is_active': True
                    },
                'PUT': self.error_message['405_PUT'],
                'HEAD': [],
                'OPTIONS': {},
                'PATCH': self.error_message['405_PATCH'],
                'DELETE': self.error_message['405_DELETE'],
                }

    def tearDown(self):
        super().tearDown()

    def test_user_api_status_code(self):
        self.status_code_is()

    def test_user_api_content_length(self):
        self.content_len_is()

    def test_user_api_content(self):
        self.content_is()

class AdminUserDetailAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /users/pk endpoint for 
    admin.
    """

    def setUp(self):
        self.maxDiff = None
        super().setUp()
        self.url = reverse('users-detail-api', args=(3,))
        self.force_authenticate(user=self.admin)
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
                'POST': 405,
                'PUT': 200,
                'HEAD': 200,
                'OPTIONS': 200,
                'PATCH': 405,
                'DELETE': 204,
                }
        self.expected_length = {
                'GET': 1,
                'PUT': 1
                }
        self.expected_content = {
                'GET': {
                    'url': 'http://testserver/billjobs/api/1.0/users/3/',
                    'username': 'bill',
                    'email': 'bill@billjobs.org',
                    'is_staff': False,
                    'is_superuser': False,
                    'groups': [
                        'http://testserver/billjobs/api/1.0/groups/2/',
                        'http://testserver/billjobs/api/1.0/groups/3/'
                        ]
                    },
                'POST': self.error_message['405_POST'],
                'PUT': {
                    'url': 'http://testserver/billjobs/api/1.0/users/3/',
                    'username': 'bar',
                    'email': 'bill@billjobs.org',
                    'is_staff': False,
                    'is_superuser': False,
                    'groups': [
                        'http://testserver/billjobs/api/1.0/groups/2/',
                        'http://testserver/billjobs/api/1.0/groups/3/'
                        ]
                    },
                'HEAD': [],
                'OPTIONS': {},
                'PATCH': self.error_message['405_PATCH'],
                'DELETE': None,
                }

    def tearDown(self):
        super().tearDown()

    def test_user_detail_api_status_code(self):
        self.status_code_is()

    def test_user_detail_api_content_length(self):
        self.content_len_is()

    def test_user_detail_api_content(self):
        self.content_is()
