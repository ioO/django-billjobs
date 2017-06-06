from rest_framework import status
from billjobs.tests.generics import GenericAPIStatusCode

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
