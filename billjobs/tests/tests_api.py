from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

class GenericAPIStatusCode(TestCase):
    """
    A generic class to test status code returned by API
    """
    fixtures=['test_api_user.yaml']

    def setUp(self):
        """
        Common vars for tests
        """
        self.admin = User.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        self.client = APIClient()
        self.url_users = reverse('users-api')
        self.url_users_detail = reverse('users-detail-api', args=(1,))

    def force_authenticate(self, user):
        """
        Force authenticate of client with user

        Parameters
        ----------
        user : django.contrib.models.User instance
        """
        self.client.force_authenticate(user=user)

    def status_code_is(self, method, url, data, status_code):
        """
        Assert that the response.status_code and status_code are equal.

        Parameters
        ----------
        method : string
            The http method to use for the request
        url : string
            The target url for the request
        data : dict
            A dictionary of data to add in request (POST, PUT)
        status_code : int
            The integer representing the status code (2xx, 3xx, 4xx, 5xx)

        Returns
        -------
        The test failed or not.
        """
        if method == 'GET':
            response = self.client.get(url, format='json')

        elif method == 'POST':
            response = self.client.post(url, data, format='json')

        elif method == 'PUT':
            response = self.client.put(url, data, format='json')

        elif method == 'DELETE':
            response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status_code)

class APITokenAuthenticationStatusCode(GenericAPIStatusCode):
    """
    Test API Token Authentication response status code
    """


    def setUp(self):
        GenericAPIStatusCode.setUp(self)
        self.url = reverse('api-token-auth')

    def test_admin_auth_token(self):
        """
        Test status code is 200 when admin use correct credential
        """
        data = {'username': self.admin.username, 'password': 'jobs'}
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url, data, status.HTTP_200_OK)

    def test_user_auth_token(self):
        """
        Test status code is 200 when user user correct credential
        """
        data = {'username': self.user.username, 'password': 'jobs'}
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url, data, status.HTTP_200_OK)

    def test_invalid_user(self):
        """
        Test invalid user get 400
        """
        data = {'username': 'foo', 'password': 'bar'}
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url, data, status.HTTP_400_BAD_REQUEST)

class APITokenAuthentication(GenericAPIStatusCode):
    """
    Test API token authentication
    """
    def setUp(self):
        GenericAPIStatusCode.setUp(self)
        self.url = reverse('api-token-auth')

    def test_admin_token_auth(self):
        """
        Test admin token auth return a valid token
        """
        data = {'username': self.admin.username, 'password': 'jobs' }
        response = self.client.post(self.url, data)
        self.assertTrue(len(response.data['token']), 20)

    def test_user_token_auth(self):
        """
        Test user api-token-auth return a valid token
        """
        data = {'username': self.user.username, 'password': 'jobs' }
        response = self.client.post(self.url, data)
        self.assertTrue(len(response.data['token']), 20)

    def test_invalid_user_get_token_error(self):
        """
        Test an invalid user do not get a token
        """
        data = {'username': 'invalid', 'password': 'jobs'}
        response = self.client.post(self.url, data)
        self.assertIn('Unable to log in with provided credentials.',
                response.data['non_field_errors'] )

class APIAnonymousPermission(GenericAPIStatusCode):
    """
    Test API anonymous level permission to endpoints
    """

    def setUp(self):
        GenericAPIStatusCode.setUp(self)
        self.url_login = reverse('rest_framework:login')

    def test_api_auth_get_is_public(self):
        """
        Test api login GET method is public
        """
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url_login, None, status.HTTP_200_OK)

    def test_api_auth_post_is_public(self):
        """
        Test api login POST method is public
        """
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url_login, None, status.HTTP_200_OK)

    def test_api_auth_token_post_is_public(self):
        """
        Test api token POST method is public
        Method return 400 with bad credentials, we test response status code is
        not 403
        """
        response = self.client.post(reverse('api-token-auth'))
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_user_get_is_not_public(self):
        """
        Test api user endpoint with GET method is not public
        Anonymous user can not list user
        """
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url_users, None, status.HTTP_401_UNAUTHORIZED
                )

    def test_api_user_post_is_public(self):
        """
        Test api user endpoint with POST method is public
        Anonymous user can create an account
        """
        data = {'username': 'gate', 'password': 'steve',
                'email': 'steve@gate.org'
                }
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url_users, data, status.HTTP_201_CREATED)

    def test_api_user_detail_get_is_not_public(self):
        """
        Test api user detail endpoint with GET method is not public
        Anonymous user can not retrieve user information
        """
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url_users_detail, None,
                status.HTTP_401_UNAUTHORIZED
                )

    def test_api_user_detail_put_is_not_public(self):
        """
        Test api user detail endpoint with PUT method is not public
        Anonymous user can not update a user instance
        """
        data = {'password': 'inject'}
        GenericAPIStatusCode.status_code_is(
                self, 'PUT', self.url_users_detail, None,
                status.HTTP_401_UNAUTHORIZED
                )

    def test_api_user_detail_delete_is_not_public(self):
        """
        Test api user detail endpoint with DELETE method is not public
        Anonymous user can not delete an user instance
        """
        GenericAPIStatusCode.status_code_is(
                self, 'DELETE', self.url_users_detail, None,
                status.HTTP_401_UNAUTHORIZED
                )

class APIUserPermission(GenericAPIStatusCode):
    """
    Test API user level permission to endpoints
    """

    def setUp(self):
        GenericAPIStatusCode.setUp(self)
        GenericAPIStatusCode.force_authenticate(self, self.user)

    def test_api_user_get_is_forbidden(self):
        """
        Test api user endpoint with GET method is forbidden for user
        User can not list user
        """
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url_users, None, status.HTTP_403_FORBIDDEN)

    def test_api_user_post_is_public(self):
        """
        Test api user endpoint with POST method is accessible
        User can create another account
        """
        data = {'username': 'gate', 'password': 'steve',
                'email': 'steve@gate.org'
                }
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url_users, data, status.HTTP_201_CREATED)

    def test_api_user_detail_get_is_ok(self):
        """
        Test api user detail endpoint with GET method is ok
        User can retrieve his own information
        """
        url = reverse('users-detail-api', args=(2,))
        GenericAPIStatusCode.status_code_is(
                self, 'GET', url, None, status.HTTP_200_OK)

    def test_api_user_detail_get_other_user_is_forbidden(self):
        """
        Test api user detail endpoint with GET method is forbidden for user
        User can not retrieves other user information
        """
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url_users_detail, None,
                status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_put_is_ok(self):
        """
        Test api user detail endpoint with POST method is ok
        User can update his user instance
        """
        url = reverse('users-detail-api', args=(2,))
        data = {'password': 'inject'}
        GenericAPIStatusCode.status_code_is(
                self, 'PUT', url, data, status.HTTP_200_OK)

    def test_api_user_detail_put_other_user_is_forbidden(self):
        """
        Test api user detail endpoint with POST method is forbidden
        User can not update other user instance
        """
        url = reverse('users-detail-api', args=(3,))
        data = {'password': 'inject'}
        GenericAPIStatusCode.status_code_is(
                self, 'PUT', url, data, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_delete_is_ok(self):
        """
        Test api user detail endpoint with DELETE method is ok
        User can delete his user instance
        """
        url = reverse('users-detail-api', args=(2,))
        GenericAPIStatusCode.status_code_is(
                self, 'DELETE', url, None, status.HTTP_204_NO_CONTENT)

    def test_api_user_detail_delete_other_user_is_forbidden(self):
        """
        Test api user detail endpoint with DELETE method is forbidden
        User can not delete other user instance
        """
        url = reverse('users-detail-api', args=(3,))
        GenericAPIStatusCode.status_code_is(
                self, 'DELETE', url, None, status.HTTP_403_FORBIDDEN)

class APIAdminPermission(GenericAPIStatusCode):
    """
    Test API admin level permission to endpoints
    """

    def setUp(self):
        GenericAPIStatusCode.setUp(self)
        GenericAPIStatusCode.force_authenticate(self, self.admin)

    def test_api_user_get_is_accessible(self):
        """
        Test api user endpoint with GET method is accessible by admin
        An admin can list user
        """
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url_users, None, status.HTTP_200_OK)

    def test_api_user_post_is_accessible(self):
        """
        Test api user endpoint with POST method is accessible by admin
        An admin can create a user
        """
        data = {'username': 'foo', 'password': 'bar', 'email': 'foo@bar.foo'}
        GenericAPIStatusCode.status_code_is(
                self, 'POST', self.url_users, data, status.HTTP_201_CREATED)

    def test_api_user_detail_get_is_accessible(self):
        """
        Test api user detail endpoint with GET method is accessible by admin
        Admin can access user instance information
        """
        url = reverse('users-detail-api', args=(2,))
        GenericAPIStatusCode.status_code_is(
                self, 'GET', self.url_users_detail, None, status.HTTP_200_OK)

    def test_api_user_detail_put_is_accessible(self):
        """
        Test api user detail endpoint with PUT method is accessible by admin
        Admin can update user instance
        """
        url = reverse('users-detail-api', args=(2,))
        data = {'firstname': 'foobar'}
        GenericAPIStatusCode.status_code_is(
                self, 'PUT', url, data, status.HTTP_200_OK)

    def test_api_user_detail_put_is_accessible(self):
        """
        Test api user detail endpoint with DELETE method is accessible by admin
        Admin can delete a user instance
        """
        url = reverse('users-detail-api', args=(2,))
        GenericAPIStatusCode.status_code_is(
                self, 'DELETE', url, None, status.HTTP_204_NO_CONTENT)
