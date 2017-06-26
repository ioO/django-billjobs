from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from billjobs.tests.generics import GenericAPITest, GenericAPIStatusCode
import collections

class AnonymousGroupAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /groups endpoint for
    anonymous user.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('groups-api')
        self.data = {
                'create': {'name': 'group name'},
                'update': {'name': 'new name'}
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
                'GET': self.error_message['authenticated'],
                'POST': self.error_message['authenticated'],
                'PUT': self.error_message['authenticated'],
                'DELETE': self.error_message['authenticated'],
                'HEAD': self.error_message['authenticated'],
                'OPTIONS': self.error_message['authenticated'],
                'PATCH': self.error_message['authenticated'],
                }

    def tearDown(self):
        super().tearDown()

    def test_group_api_status_code(self):
        self.status_code_is()

    def test_group_api_content(self):
        self.content_is()

class AnonymousGroupDetailAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /groups/pk endpoint for
    anonymous user.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('groups-detail-api', args=(1,))
        self.data = {
                'create': {'name': 'group name'},
                'update': {'name': 'new name'}
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
                'GET': self.error_message['authenticated'],
                'POST': self.error_message['authenticated'],
                'PUT': self.error_message['authenticated'],
                'DELETE': self.error_message['authenticated'],
                'HEAD': self.error_message['authenticated'],
                'OPTIONS': self.error_message['authenticated'],
                'PATCH': self.error_message['authenticated'],
                }

    def tearDown(self):
        super().tearDown()

    def test_group_api_status_code(self):
        self.status_code_is()

    def test_group_api_content(self):
        self.content_is()

class UserGroupAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /groups endpoint for
    authenticated user.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('groups-api')
        self.force_authenticate(user=self.bill)
        self.data = {
                'create': {'name': 'group name'},
                'update': {'name': 'new name'}
                }
        self.expected_status = {
                'GET': 200,
                'POST': 403,
                'PUT': 403,
                'DELETE': 403,
                'HEAD': 403,
                'OPTIONS': 403,
                'PATCH': 403,
                }
        self.expected_content = {
                'GET': [
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/2/",
                        "name": "user group",
                        "permissions": []
                        }),
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/3/",
                        "name": "bill group",
                        "permissions": []
                        })
                    ],
                'POST': self.error_message['forbidden'],
                'PUT': self.error_message['forbidden'],
                'DELETE': self.error_message['forbidden'],
                'HEAD': self.error_message['forbidden'],
                'OPTIONS': self.error_message['forbidden'],
                'PATCH': self.error_message['forbidden'],
                }

    def tearDown(self):
        super().tearDown()

    def test_group_api_status_code(self):
        self.status_code_is()

    def test_group_api_content(self):
        self.content_is()

    def test_user_with_no_group_response_data(self):
        """
        Test the data in response when the user has no group
        """
        self.force_authenticate(user=self.nogroupuser)
        self.expected_content['GET'] = list()
        self.content_is()

class UserGroupDetailAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /groups endpoint for
    authenticated user.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('groups-detail-api', args=(2,))
        self.force_authenticate(user=self.bill)
        self.data = {
                'create': {'name': 'group name'},
                'update': {'name': 'bill jobs'}
                }
        self.expected_status = {
                'GET': 200,
                'POST': 403,
                'PUT': 403,
                'DELETE': 403,
                'HEAD': 403,
                'OPTIONS': 403,
                'PATCH': 403,
                }
        self.expected_content = {
                'GET': {
                    "url": "http://testserver/billjobs/api/1.0/groups/2/",
                    "name": "user group",
                    "permissions": []
                    },
                'POST': self.error_message['forbidden'],
                'PUT': self.error_message['forbidden'],
                'DELETE': self.error_message['forbidden'],
                'HEAD': self.error_message['forbidden'],
                'OPTIONS': self.error_message['forbidden'],
                'PATCH': self.error_message['forbidden'],
                }

    def tearDown(self):
        super().tearDown()

    def test_group_api_status_code(self):
        self.status_code_is()

    def test_group_api_content(self):
        self.content_is()

    def test_user_with_no_group_response_data(self):
        """
        Test the data in response when the user has no group
        """
        self.force_authenticate(user=self.nogroupuser)
        self.expected_content['GET'] = dict()
        self.content_is()

    def test_user_can_not_access_group_he_do_not_belongs(self):
        """
        Test an authenticated user can not access group of another user
        Bill can not access group detail of admin
        """
        self.url = reverse('groups-detail-api', args=(1,))
        self.expected_status['GET'] = 403
        self.expected_content['GET'] = self.error_message['forbidden']
        self.status_code_is()
        self.content_is()

class AdminGroupAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /groups endpoint for
    authenticated admin.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('groups-api')
        self.force_authenticate(user=self.admin)
        self.data = {
                'create': {'name': 'new group'},
                'update': {'name': 'admin jobs'}
                }
        self.expected_status = {
                'GET': 200,
                'POST': 201,
                'PUT': 405,
                'DELETE': 405,
                'HEAD': 200,
                'OPTIONS': 200,
                'PATCH': 405,
                }
        self.expected_content = {
                'GET': [
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/1/",
                        "name": "admin group",
                        "permissions": []
                        }),
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/2/",
                        "name": "user group",
                        "permissions": []
                        }),
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/3/",
                        "name": "bill group",
                        "permissions": []
                        }),
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/4/",
                        "name": "steve group",
                        "permissions": []
                        }),
                    ],
                'POST': {
                    "url": "http://testserver/billjobs/api/1.0/groups/5/",
                    "name": "new group",
                    "permissions": []
                    },
                'PUT': {
                    'detail':
                        'Method "PUT" not allowed.'
                    },
                'DELETE': {
                    'detail':
                        'Method "DELETE" not allowed.'
                    },
                'HEAD': [
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/1/",
                        "name": "admin group",
                        "permissions": []
                        }),
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/2/",
                        "name": "user group",
                        "permissions": []
                        }),
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/3/",
                        "name": "bill group",
                        "permissions": []
                        }),
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/4/",
                        "name": "steve group",
                        "permissions": []
                        }),
                    collections.OrderedDict({
                        "url": "http://testserver/billjobs/api/1.0/groups/5/",
                        "name": "new group",
                        "permissions": []
                        }),
                    ],
                'OPTIONS': {
                    'name': 'Group Api',
                    'description': 'API endpoint to list or create groups',
                    'renders': [
                        'application/json',
                        'text/html'
                        ],
                    'parses': [
                        'application/json',
                        'application/x-www-form-urlencoded',
                        'multipart/form-data'
                        ]
                    },
                'PATCH': {
                    'detail':
                        'Method "PATCH" not allowed.'
                    },
                }

    def tearDown(self):
        super().tearDown()

    def test_group_api_status_code(self):
        self.status_code_is()

    def test_group_api_content(self):
        self.content_is()

class AdminGroupDetailAPITest(GenericAPITest):
    """
    Tests status code and response content returned by /groups/pk endpoint for
    authenticated admin.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse('groups-detail-api', args=(4,))
        self.force_authenticate(user=self.admin)
        self.data = {
                'create': {'name': 'new group'},
                'update': {'name': 'admin jobs'}
                }
        self.expected_status = {
                'GET': 200,
                'POST': 405,
                'PUT': 200,
                'DELETE': 204,
                'HEAD': 404,
                'OPTIONS': 200,
                'PATCH': 405,
                }
        self.expected_content = {
                'GET': {
                    "url": "http://testserver/billjobs/api/1.0/groups/4/",
                    "name": "steve group",
                    "permissions": []
                    },
                'POST': {
                    'detail':
                        'Method "POST" not allowed.'
                    },
                'PUT': {
                    "url": "http://testserver/billjobs/api/1.0/groups/4/",
                    "name": "admin jobs",
                    "permissions": []
                    },
                'DELETE': None,
                'OPTIONS': {
                    'name': 'Group Detail Api',
                    'description': 'API endpoint that allow admin and user to retrieve, update and delete a \ngroup',
                    'renders': [
                        'application/json',
                        'text/html'
                        ],
                    'parses': [
                        'application/json',
                        'application/x-www-form-urlencoded',
                        'multipart/form-data'
                        ]
                    },
                'PATCH': {
                    'detail':
                        'Method "PATCH" not allowed.'
                    },
                }

    def tearDown(self):
        super().tearDown()

    def test_group_api_status_code(self):
        self.status_code_is()

    def test_group_api_content(self):
        self.content_is()

    def test_group_detail_api_head_status(self):
        """
        Generic class do a DELETE before a HEAD so the object is not existing
        This test only do a HEAD request
        """
        self.expected_status = {'HEAD': 200}
        self.status_code_is()

