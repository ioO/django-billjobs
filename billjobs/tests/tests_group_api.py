from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from billjobs.tests.generics import GenericAPITest, GenericAPIStatusCode

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
                'PATCH': 401,
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
