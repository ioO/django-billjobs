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

class APIAnonymousPermission(TestCase):
    """
    Test API anonymous level permission to endpoints
    """

    def setUp(self):
        self.client = APIClient()

    def test_api_auth_get_is_public(self):
        """
        Test api login GET method is public
        """
        response = self.client.get(reverse('rest_framework:login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_auth_post_is_public(self):
        """
        Test api login POST method is public
        """
        response = self.client.post(reverse('rest_framework:login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        response = self.client.get(reverse('users-api'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_user_post_is_public(self):
        """
        Test api user endpoint with POST method is public
        Anonymous user can create an account
        """
        data = {'username': 'gate', 'password': 'steve',
                'email': 'steve@gate.org'
                }
        response = self.client.post(reverse('users-api'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_user_detail_get_is_not_public(self):
        """
        Test api user detail endpoint with GET method is not public
        Anonymous user can not retrieve user information
        """
        response = self.client.get(reverse('users-detail-api', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_user_detail_put_is_not_public(self):
        """
        Test api user detail endpoint with POST method is not public
        Anonymous user can not update a user instance
        """
        response = self.client.post(reverse('users-detail-api', args=(1,)), {'password': 'inject'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_user_detail_delete_is_not_public(self):
        """
        Test api user detail endpoint with DELETE method is not public
        Anonymous user can not delete an user instance
        """
        response = self.client.delete(reverse('users-detail-api', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class APIUserPermission(TestCase):
    """
    Test API user level permission to endpoints
    """

    fixtures = ['test_api_user.yaml']

    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_api_user_get_is_forbidden(self):
        """
        Test api user endpoint with GET method is forbidden for user
        User can not list user
        """
        response = self.client.get(reverse('users-api'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_user_post_is_public(self):
        """
        Test api user endpoint with POST method is accessible
        User can create another account
        """
        data = {'username': 'gate', 'password': 'steve',
                'email': 'steve@gate.org'
                }
        response = self.client.post(reverse('users-api'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_user_detail_get_is_forbidden(self):
        """
        Test api user detail endpoint with GET method is forbidden for user
        User can not retrieves his user information
        """
        response = self.client.get(reverse('users-detail-api', args=(2,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_get_other_user_is_forbidden(self):
        """
        Test api user detail endpoint with GET method is forbidden for user
        User can not retrieves other user information
        """
        response = self.client.get(reverse('users-detail-api', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_put_is_forbidden(self):
        """
        Test api user detail endpoint with POST method is forbidden
        User can not update his user instance
        """
        response = self.client.put(reverse('users-detail-api', args=(2,)), {'password': 'inject'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_put_other_user_is_forbidden(self):
        """
        Test api user detail endpoint with POST method is forbidden
        User can not update other user instance
        """
        response = self.client.put(reverse('users-detail-api', args=(3,)), {'password': 'inject'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_delete_is_forbidden(self):
        """
        Test api user detail endpoint with DELETE method is forbidden
        User can not delete his user instance
        """
        response = self.client.delete(reverse('users-detail-api', args=(2,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_delete_other_user_is_forbidden(self):
        """
        Test api user detail endpoint with DELETE method is forbidden
        User can not delete other user instance
        """
        response = self.client.delete(reverse('users-detail-api', args=(3,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class APIAdminPermission(TestCase):
    """
    Test API admin level permission to endpoints
    """

    fixtures = ['test_api_user.yaml']

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_api_user_get_is_accessible(self):
        """
        Test api user endpoint with GET method is accessible by admin
        An admin can list user
        """
        response = self.client.get(reverse('users-api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_post_is_accessible(self):
        """
        Test api user endpoint with POST method is accessible by admin
        An admin can create a user
        """
        data = {'username': 'foo', 'password': 'bar', 'email': 'foo@bar.foo'}
        response = self.client.post(reverse('users-api'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_user_detail_get_is_accessible(self):
        """
        Test api user detail endpoint with GET method is accessible by admin
        Admin can access user instance information
        """
        response = self.client.get(reverse('users-detail-api', args=(2,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_detail_put_is_accessible(self):
        """
        Test api user detail endpoint with PUT method is accessible by admin
        Admin can update user instance
        """
        data = {'firstname': 'foobar'}
        response = self.client.put(reverse('users-detail-api', args=(2,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_detail_put_is_accessible(self):
        """
        Test api user detail endpoint with DELETE method is accessible by admin
        Admin can delete a user instance
        """
        response = self.client.delete(reverse('users-detail-api', args=(2,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
