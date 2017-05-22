from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, \
        force_authenticate
from billjobs.views import UserAPI, UserDetailAPI
from billjobs.tests.generics import GenericAPIStatusCode
import json
import io

def get_json(response):
        """
        Return a json from a response content
        """
        return json.load(io.StringIO(response.content.decode()))

class UserAdminAPIStatusCode(GenericAPIStatusCode):
    """
    Test status code returned by endpoints
    Status code related to permission are tested in tests_api.py
    """

    fixtures = ['test_api_user.yaml']

    def setUp(self):
        GenericAPIStatusCode.setUp(self)
        GenericAPIStatusCode.force_authenticate(self, self.admin)
        self.url = self.endpoints['users']

    def test_user_admin_get_is_200(self):
        """
        Test api user admin endpoints with GET method is HTTP_200_OK
        """
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url, None, status.HTTP_200_OK)

    def test_user_admin_post_is_201(self):
        """
        Test api user admin endpoints with POST method is HTTP_201_CREATED
        """
        data = {'username': 'foo', 'password': 'bar', 'email': 'foo@bar.org'}
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url, data, status.HTTP_201_CREATED)

    def test_user_admin_post_is_400(self):
        """
        Test api user admin endpoints with POST method is HTTP_400_BAD_REQUEST
        when input data are incorrect
        """
        data = {'username': 'foo'}
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url, data, status.HTTP_400_BAD_REQUEST)

    def test_user_admin_put_is_405(self):
        """
        Test api user admin endpoints with PUT return
        HTTP_405_METHOD_NOT_ALLOWED
        """
        data = {'username': 'foo'}
        GenericAPIStatusCode.status_code_is(
                self, 'PUT', self.url, data, status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def test_user_admin_delete_is_405(self):
        """
        Test api user admin endpoints with DELETE return
        HTTP_405_METHOD_NOT_ALLOWED
        """
        response = self.client.delete(self.url)
        GenericAPIStatusCode.status_code_is(
                self, 'DELETE', self.url, None,
                status.HTTP_405_METHOD_NOT_ALLOWED)

class UserAdminDetailAPIStatusCode(GenericAPIStatusCode):
    """
    Test user admin detail api response status code
    """

    fixtures=['test_api_user.yaml']

    def setUp(self):
        GenericAPIStatusCode.setUp(self)
        GenericAPIStatusCode.force_authenticate(self, user=self.admin)
        self.url = GenericAPIStatusCode.endpoint_url(
                self, 'users-detail-api', args=(2,))
        self.url_bad_user = GenericAPIStatusCode.endpoint_url(
                self, 'users-detail-api', args=(1234,))

    def test_user_detail_get_is_200(self):
        """
        Test api user detail endpoints with GET return HTTP_200_OK
        """
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url, None, status.HTTP_200_OK)

    def test_user_detail_get_is_404_with_bad_pk(self):
        """
        Test api user detail endpoints with GET return HTTP_404_NOT_FOUND
        when user pk does not exist.
        Use a customized url with a user pk that doesn't exist
        """
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url_bad_user, None, status.HTTP_404_NOT_FOUND
                )

    def test_user_detail_put_is_200(self):
        """
        Test api user detail endpoints with PUT method return HTTP_200_OK
        """
        data = {'username': 'foo', 'last_name': 'bar'}
        GenericAPIStatusCode.status_code_is(
                self, 'PUT', self.url, data, status.HTTP_200_OK)

    def test_user_detail_put_is_404_with_bad_pk(self):
        """
        Test api user detail endpoints with PUT return HTTP_404_NOT_FOUND
        when user pk does not exist
        Use a customized url with a user pk that doesn't exist
        """
        data = {'username': 'foo', 'last_name': 'bar'}
        GenericAPIStatusCode.status_code_is(
                self, 'PUT', self.url_bad_user, data, status.HTTP_404_NOT_FOUND
                )

    def test_user_detail_put_is_400_with_wrong_data(self):
        """
        Test api user detail endpoints with PUT return HTTP_400_BAD_REQUEST
        with wrong data in json (here username already exists)
        """
        data = {'username': 'bill', 'last_name': 'bar',
                'not_a_field': 'hello'}
        GenericAPIStatusCode.status_code_is(
                self, 'PUT', self.url, data, status.HTTP_400_BAD_REQUEST)

    def test_user_detail_delete_is_204(self):
        """
        Test api user detail endpoints with DELETE method return
        HTTP_204_NO_CONTENT
        """
        GenericAPIStatusCode.status_code_is(
                self, 'DELETE', self.url, None, status.HTTP_204_NO_CONTENT)

    def test_user_detail_delete_is_404_with_bad_pk(self):
        """
        Test api user detail endpoints with DELETE return HTTP_404_NOT_FOUND
        when user pk does not exist
        """
        GenericAPIStatusCode.status_code_is(
                self, 'DELETE', self.url_bad_user, None,
                status.HTTP_404_NOT_FOUND)

    def test_user_detail_post_is_405(self):
        """
        Test api user detail endpoints with POST return
        HTTP_405_METHOD_NOT_ALLOWED
        """
        data = {'first_name': 'foo'}
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url, data,
                status.HTTP_405_METHOD_NOT_ALLOWED)

class UserAdminAPIResponseContent(TestCase):
    """
    Test response content returned by endpoints
    """

    fixtures = ['test_api_user.yaml']

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.url = reverse('users-api')

    def test_user_admin_get_list(self):
        """
        Test api user admin endpoints with GET method return a list
        Fixtures data contain 3 users, we expect a list of 3 user in json
        """
        json_data = get_json(self.client.get(self.url))
        self.assertEqual(len(json_data), 3)

    def test_user_admin_post_return_user_information(self):
        """
        Test api user admin endpoints with POST method return json with
        user information
        """
        data = {'username': 'foo', 'password': 'bar', 'email': 'foo@bar.org'}
        json_data = get_json(self.client.post(self.url, data))
        for key in ('url', 'password', 'last_login', 'is_superuser',
                'username', 'first_name', 'last_name', 'email', 'is_staff',
                'is_active', 'date_joined', 'groups', 'user_permissions'):
            self.assertTrue(key in json_data.keys())
        self.assertEqual(json_data['username'], 'foo')
        self.assertEqual(json_data['email'], 'foo@bar.org')

    def test_user_admin_post_return_required_field(self):
        """
        Test api user admin endpoint with POST method return errors
        and required fields
        """
        data = {'first_name': 'foobar'}
        json_data = get_json(self.client.post(self.url, data))
        for key in ('username', 'password'):
            self.assertTrue(key in json_data.keys())
        self.assertIn('This field is required.', json_data['username'])
        self.assertIn('This field is required.', json_data['password'])

class UserDetailAdminAPIResponseContent(TestCase):
    """
    Test user detail api response content
    """

    fixtures = ['test_api_user.yaml']

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.url = reverse('users-detail-api', args=[2])

    def test_user_detail_admin_get_user_information(self):
        """
        Test api user admin detail endpoint with GET method return user
        information
        """
        json_data = get_json(self.client.get(self.url))
        for key in ('url', 'password', 'last_login', 'is_superuser',
                'username', 'first_name', 'last_name', 'email', 'is_staff',
                'is_active', 'date_joined', 'groups', 'user_permissions'):
            self.assertTrue(key in json_data.keys())
        self.assertEqual(json_data['username'], 'jobs')
        self.assertEqual(json_data['email'], 'jobs@billjobs.org')

    def test_user_detail_put_return_information(self):
        """
        Test api user detail endpoint with PUT method return user with new
        information
        """
        data = {'last_name': 'bar'}
        json_data = get_json(self.client.put(self.url, data))
        for key in ('url', 'password', 'last_login', 'is_superuser',
                'username', 'first_name', 'last_name', 'email', 'is_staff',
                'is_active', 'date_joined', 'groups', 'user_permissions'):
            self.assertTrue(key in json_data.keys())
        self.assertEqual(json_data['last_name'], 'bar')
        self.assertEqual(json_data['username'], 'jobs')
        self.assertEqual(json_data['email'], 'jobs@billjobs.org')

    def test_user_detail_put_return_error_when_duplicate_username(self):
        """
        Test api user detail endpoint with PUT method return an error when
        an username already exists
        information
        """
        data = {'username': 'bill'}
        json_data = get_json(self.client.put(self.url, data))
        self.assertIn('A user with that username already exists.',
                json_data['username'])

