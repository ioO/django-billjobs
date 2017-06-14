from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from billjobs.tests.generics import GenericAPITest, GenericAPIStatusCode

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
        self.force_authenticate(user=self.user)
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
        pass
        #self.content_is()

