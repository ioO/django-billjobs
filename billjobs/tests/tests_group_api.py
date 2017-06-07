from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from billjobs.tests.generics import GenericAPIStatusCode

class GenericAPITest(APITestCase):
    """
    Generic Test class to test an API endpoint
    """
    fixtures = ['test_api_user.yaml']

    def setUp(self):
        self.url = None
        self.client = APIClient()
        self.admin = User.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        self.data = {
                'create': None,
                'update': None,
                }
        self.expected_status = {
                'GET': None,
                'POST': None,
                'PUT': None,
                'DELETE': None,
                'OPTIONS': None,
                'HEAD': None,
                'PATCH': None,
                }

    def status_code_is(self):
        for method, status_code in self.expected_status.items():
            if method == 'GET':
                response = self.client.get(self.url, format='json')
            elif method == 'POST':
                response = self.client.post(
                        self.url, self.data['create'], format='json')
            elif method == 'PUT':
                response = self.client.put(
                        self.url, self.data['update'], format='json')
            elif method == 'DELETE':
                response = self.client.delete(self.url, format='json')
            elif method == 'HEAD':
                response = self.client.head(self.url, format='json')
            elif method == 'OPTIONS':
                response = self.client.options(self.url, format='json')

            self.assertEqual(response.status_code, status_code,
                    '{0} method expected status code {1}'.format(
                        method, status_code)
                    )

class AnonymousGroupAPITest(GenericAPITest):
    """
    Test group api test
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
                }

    def test_group_api_status_code(self):
        self.status_code_is()

class GroupAPIAnonymousStatusCode(GenericAPIStatusCode):
    """
    Tests status code returned by /groups endpoint for anonymous user
    Permissions are tested in tests_api.py
    """

    def setUp(self):
        super().setUp()
        self.url = self.endpoints['groups']
        self.data = {'name': 'group name'}

    def test_api_group_put_is_405(self):
        """
        Test group api with PUT method return HTTP_405_METHOD_NOT_ALLOWED
        """
        super().status_code_is(
                'PUT', self.url, self.data, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_group_delete_is_405(self):
        """
        Test group api with DELETE method return HTTP_405_METHOD_NOT_ALLOWED
        """
        super().status_code_is(
                'DELETE', self.url, None, status.HTTP_405_METHOD_NOT_ALLOWED)

class GroupAPIUserStatusCode(GenericAPIStatusCode):
    """
    Tests status code returned by /groups endpoint for user
    Permissions are tested in tests_api.py
    """

    def setUp(self):
        super().setUp()
        super().force_authenticate(self.user)
        self.url = self.endpoints['groups']
        self.data = {'name': 'group name'}

    def test_api_group_put_is_405(self):
        """
        Test group api with PUT method return HTTP_405_METHOD_NOT_ALLOWED
        """
        super().status_code_is(
                'PUT', self.url, self.data, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_group_delete_is_405(self):
        """
        Test group api with DELETE method return HTTP_405_METHOD_NOT_ALLOWED
        """
        super().status_code_is(
                'DELETE', self.url, None, status.HTTP_405_METHOD_NOT_ALLOWED)

class GroupAPIAdminStatusCode(GenericAPIStatusCode):
    """
    Tests status code returned by /groups endpoint for admin
    """

    def setUp(self):
        super().setUp()
        super().force_authenticate(self.admin)
        self.url = self.endpoints['groups']
        self.data = {'name': 'group name'}

    def test_api_group_put_is_405(self):
        """
        Test group api with PUT method return HTTP_405_METHOD_NOT_ALLOWED
        """
        super().status_code_is(
                'PUT', self.url, self.data, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_group_delete_is_405(self):
        """
        Test group api with DELETE method return HTTP_405_METHOD_NOT_ALLOWED
        """
        super().status_code_is(
                'DELETE', self.url, self.data,
                status.HTTP_405_METHOD_NOT_ALLOWED
                )
