from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

class APIStatusCode(TestCase):
    """
    Test user API response status code
    """

    fixtures=['test_api_user.yaml']

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        self.client = APIClient()

    def test_admin_auth_token(self):
        """
        Test status code is 200 when admin use correct credential
        """
        data = {'username': self.admin.username, 'password': 'jobs'}
        response = self.client.post(reverse('api-token-auth'), data,
                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_auth_token(self):
        """
        Test status code is 200 when user user correct credential
        """
        data = {'username': self.user.username, 'password': 'jobs'}
        response = self.client.post(reverse('api-token-auth'), data,
                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user(self):
        """
        Test invalid user get 400
        """
        data = {'username': 'foo', 'password': 'bar'}
        response = self.client.post(reverse('api-token-auth'), data,
                format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class APITokenAuthentication(TestCase):
    """
    Test API token authentication
    """
    fixtures=['test_api_user.yaml']

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        self.client = APIClient()
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

class APIPermission(TestCase):
    """
    Test API user level permission to endpoints
    """
    fixtures=['test_api_user.yaml']

    def setUp(self):
        pass

