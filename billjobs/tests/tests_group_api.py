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
                'GET': {
                    'detail': 'Authentication credentials were not provided.'},
                'POST': {
                    'detail': 'Authentication credentials were not provided.'},
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
                'GET': {
                    'detail': 'Authentication credentials were not provided.'},
                'POST': {
                    'detail': 'Authentication credentials were not provided.'},
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
                'POST': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'PUT': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'DELETE': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'HEAD': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'OPTIONS': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'PATCH': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
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
                'POST': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'PUT': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'DELETE': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'HEAD': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'OPTIONS': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
                'PATCH': {
                    'detail':
                        'You do not have permission to perform this action.'
                    },
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
