from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from billjobs.tests.generics import GenericAPIStatusCode

class APITokenAuthenticationStatusCode(GenericAPIStatusCode):
    """
    Test API Token Authentication response status code
    """

    def setUp(self):
        super().setUp()
        self.url = self.endpoints['api-token-auth']

    def test_admin_auth_token(self):
        """
        Test status code is 200 when admin use correct credential
        """
        data = {'username': self.admin.username, 'password': 'jobs'}
        super().status_code_is('POST', self.url, data, status.HTTP_200_OK)

    def test_user_auth_token(self):
        """
        Test status code is 200 when user user correct credential
        """
        data = {'username': self.user.username, 'password': 'jobs'}
        super().status_code_is('POST', self.url, data, status.HTTP_200_OK)

    def test_invalid_user(self):
        """
        Test invalid user get 400
        """
        data = {'username': 'foo', 'password': 'bar'}
        super().status_code_is('POST', self.url, data, status.HTTP_400_BAD_REQUEST)

class APITokenAuthentication(GenericAPIStatusCode):
    """
    Test API token authentication
    """
    def setUp(self):
        super().setUp()
        self.url = self.endpoints['api-token-auth']

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
        super().setUp()
        self.url_login = reverse('rest_framework:login')

    def test_api_auth_get_is_public(self):
        """
        Test api login GET method is public
        """
        super().status_code_is(
                'GET', self.url_login, None, status.HTTP_200_OK)

    def test_api_auth_post_is_public(self):
        """
        Test api login POST method is public
        """
        super().status_code_is(
                'POST', self.url_login, None, status.HTTP_200_OK)

    def test_api_auth_token_post_is_public(self):
        """
        Test api token POST method is public
        Method return 400 with bad credentials, we test response status code is
        not 403
        """
        response = self.client.post(reverse('api-token-auth'))
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

