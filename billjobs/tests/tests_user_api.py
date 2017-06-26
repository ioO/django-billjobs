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
                'GET': self.error_message['authenticated'],
                'POST': {
                    'url': 'http://testserver/billjobs/api/1.0/users/6/',
                    'username': 'foo',
                    'password': 'bar',
                    'email': 'foo@bar.org'
                    },
                'PUT': self.error_message['authenticated'],
                'DELETE': self.error_message['authenticated'],
                'HEAD': self.error_message['authenticated'],
                'OPTIONS': self.error_message['authenticated'],
                'PATCH': self.error_message['authenticated'],
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
                'PUT': self.error_message['forbidden'],
                'DELETE': self.error_message['forbidden'],
                'HEAD': self.error_message['forbidden'],
                'OPTIONS': self.error_message['forbidden'],
                'PATCH': self.error_message['forbidden'],
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
                'POST': self.error_message['forbidden'],
                'PUT': {
                    'url': 'http://testserver/billjobs/api/1.0/users/3/',
                    'username': 'bar',
                    'email': 'bill@billjobs.org'
                    },
                'DELETE': None,
                'HEAD': self.error_message['forbidden'],
                'OPTIONS': self.error_message['forbidden'],
                'PATCH': self.error_message['forbidden'],
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
        self.expected_content = { 'GET': self.error_message['forbidden'] }
        self.url = reverse('users-detail-api', args=(4,))
        self.status_code_is()
        self.content_is()

    def test_user_can_not_update_other_user(self):
        """
        An authenticated user can not update information of another user
        """
        self.expected_status = { 'PUT': 403 }
        self.expected_content = { 'PUT': self.error_message['forbidden'] }
        self.url = reverse('users-detail-api', args=(4,))
        self.status_code_is()
        self.content_is()

    def test_user_can_not_delete_other_user(self):
        """
        An authenticated user can not delete information of another user
        """
        self.expected_status = { 'DELETE': 403 }
        self.expected_content = { 'DELETE': self.error_message['forbidden'] }
        self.url = reverse('users-detail-api', args=(4,))
        self.status_code_is()
        self.content_is()

#class UserAdminAPIStatusCode(GenericAPIStatusCode):
#    """
#    Test status code returned by endpoints
#    Status code related to permission are tested in tests_api.py
#    """
#
#    fixtures = ['test_api_user.yaml']
#
#    def setUp(self):
#        super().setUp()
#        super().force_authenticate(self.admin)
#        self.url = self.endpoints['users']
#
#    def test_user_admin_get_is_200(self):
#        """
#        Test api user admin endpoints with GET method is HTTP_200_OK
#        """
#        super().status_code_is('GET', self.url, None, status.HTTP_200_OK)
#
#    def test_user_admin_post_is_201(self):
#        """
#        Test api user admin endpoints with POST method is HTTP_201_CREATED
#        """
#        data = {'username': 'foo', 'password': 'bar', 'email': 'foo@bar.org'}
#        super().status_code_is('POST', self.url, data, status.HTTP_201_CREATED)
#
#    def test_user_admin_post_is_400(self):
#        """
#        Test api user admin endpoints with POST method is HTTP_400_BAD_REQUEST
#        when input data are incorrect
#        """
#        data = {'username': 'foo'}
#        super().status_code_is(
#                'POST', self.url, data, status.HTTP_400_BAD_REQUEST)
#
#    def test_user_admin_put_is_405(self):
#        """
#        Test api user admin endpoints with PUT return
#        HTTP_405_METHOD_NOT_ALLOWED
#        """
#        data = {'username': 'foo'}
#        super().status_code_is(
#                'PUT', self.url, data, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#    def test_user_admin_delete_is_405(self):
#        """
#        Test api user admin endpoints with DELETE return
#        HTTP_405_METHOD_NOT_ALLOWED
#        """
#        response = self.client.delete(self.url)
#        super().status_code_is(
#                'DELETE', self.url, None, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#class UserAdminDetailAPIStatusCode(GenericAPIStatusCode):
#    """
#    Test user admin detail api response status code
#    """
#
#    fixtures=['test_api_user.yaml']
#
#    def setUp(self):
#        super().setUp()
#        super().force_authenticate(user=self.admin)
#        self.url = super().endpoint_url(
#                'users-detail-api', args=(2,))
#        self.url_bad_user = super().endpoint_url(
#                'users-detail-api', args=(1234,))
#
#    def test_user_detail_get_is_200(self):
#        """
#        Test api user detail endpoints with GET return HTTP_200_OK
#        """
#        super().status_code_is('GET', self.url, None, status.HTTP_200_OK)
#
#    def test_user_detail_get_is_404_with_bad_pk(self):
#        """
#        Test api user detail endpoints with GET return HTTP_404_NOT_FOUND
#        when user pk does not exist.
#        Use a customized url with a user pk that doesn't exist
#        """
#        super().status_code_is(
#                'GET', self.url_bad_user, None, status.HTTP_404_NOT_FOUND)
#
#    def test_user_detail_put_is_200(self):
#        """
#        Test api user detail endpoints with PUT method return HTTP_200_OK
#        """
#        data = {'username': 'foo', 'last_name': 'bar'}
#        super().status_code_is('PUT', self.url, data, status.HTTP_200_OK)
#
#    def test_user_detail_put_is_404_with_bad_pk(self):
#        """
#        Test api user detail endpoints with PUT return HTTP_404_NOT_FOUND
#        when user pk does not exist
#        Use a customized url with a user pk that doesn't exist
#        """
#        data = {'username': 'foo', 'last_name': 'bar'}
#        super().status_code_is(
#                'PUT', self.url_bad_user, data, status.HTTP_404_NOT_FOUND)
#
#    def test_user_detail_put_is_400_with_wrong_data(self):
#        """
#        Test api user detail endpoints with PUT return HTTP_400_BAD_REQUEST
#        with wrong data in json (here username already exists)
#        """
#        data = {'username': 'bill', 'last_name': 'bar',
#                'not_a_field': 'hello'}
#        super().status_code_is(
#                'PUT', self.url, data, status.HTTP_400_BAD_REQUEST)
#
#    def test_user_detail_delete_is_204(self):
#        """
#        Test api user detail endpoints with DELETE method return
#        HTTP_204_NO_CONTENT
#        """
#        super().status_code_is(
#                'DELETE', self.url, None, status.HTTP_204_NO_CONTENT)
#
#    def test_user_detail_delete_is_404_with_bad_pk(self):
#        """
#        Test api user detail endpoints with DELETE return HTTP_404_NOT_FOUND
#        when user pk does not exist
#        """
#        super().status_code_is(
#                'DELETE', self.url_bad_user, None, status.HTTP_404_NOT_FOUND)
#
#    def test_user_detail_post_is_405(self):
#        """
#        Test api user detail endpoints with POST return
#        HTTP_405_METHOD_NOT_ALLOWED
#        """
#        data = {'first_name': 'foo'}
#        super().status_code_is(
#                'POST', self.url, data, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#class UserAdminAPIResponseContent(GenericAPIResponseContent):
#    """
#    Test response content returned by endpoints
#    """
#
#    def setUp(self):
#        super().setUp()
#        super().force_authenticate(user=self.admin)
#        self.url = self.endpoints['users']
#
#    def test_user_admin_get_list(self):
#        """
#        Test api user admin endpoints with GET method return a list
#        Fixtures data contain 4 users, we expect a list of 4 user in json
#        """
#        json_data = super().get_json('GET', self.url)
#        self.assertEqual(len(json_data), 4)
#
#    def test_user_admin_post_return_user_information(self):
#        """
#        Test api user admin endpoints with POST method return json with
#        user information
#        """
#        data = {'username': 'foo', 'password': 'bar', 'email': 'foo@bar.org'}
#        json_data = super().get_json('POST', self.url, data)
#        for key in self.user_keys:
#            self.assertTrue(key in json_data.keys())
#        self.assertEqual(json_data['username'], 'foo')
#        self.assertEqual(json_data['email'], 'foo@bar.org')
#
#    def test_user_admin_post_return_required_field(self):
#        """
#        Test api user admin endpoint with POST method return errors
#        and required fields
#        """
#        data = {'first_name': 'foobar'}
#        json_data = super().get_json('POST', self.url, data)
#        for key in ('username', 'password'):
#            self.assertTrue(key in json_data.keys())
#        self.assertIn('This field is required.', json_data['username'])
#        self.assertIn('This field is required.', json_data['password'])
#
#class UserDetailAdminAPIResponseContent(GenericAPIResponseContent):
#    """
#    Test user detail api response content
#    """
#
#    fixtures = ['test_api_user.yaml']
#
#    def setUp(self):
#        super().setUp()
#        super().force_authenticate(user=self.admin)
#        self.url = self.endpoints['users-detail']
#
#    def test_user_detail_admin_get_user_information(self):
#        """
#        Test api user admin detail endpoint with GET method return user
#        information
#        """
#        json_data = super().get_json('GET', self.url)
#        for key in ('url', 'password', 'last_login', 'is_superuser',
#                'username', 'first_name', 'last_name', 'email', 'is_staff',
#                'is_active', 'date_joined', 'groups', 'user_permissions'):
#            self.assertTrue(key in json_data.keys())
#        self.assertEqual(json_data['username'], 'steve')
#        self.assertEqual(json_data['email'], 'steve@billjobs.org')
#
#    def test_user_detail_put_return_information(self):
#        """
#        Test api user detail endpoint with PUT method return user with new
#        information
#        """
#        data = {'last_name': 'bar'}
#        json_data = super().get_json('PUT', self.url, data)
#        for key in self.user_keys:
#            self.assertTrue(key in json_data.keys())
#        self.assertEqual(json_data['last_name'], 'bar')
#        self.assertEqual(json_data['username'], 'steve')
#        self.assertEqual(json_data['email'], 'steve@billjobs.org')
#
#    def test_user_detail_put_return_error_when_duplicate_username(self):
#        """
#        Test api user detail endpoint with PUT method return an error when
#        an username already exists
#        information
#        """
#        data = {'username': 'bill'}
#        json_data = super().get_json('PUT', self.url, data)
#        self.assertIn('A user with that username already exists.',
#                json_data['username'])
#
