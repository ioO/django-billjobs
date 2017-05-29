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
        self.url_users = self.endpoints['users']
        self.url_users_detail = self.endpoints['users-detail']
        self.url_groups = self.endpoints['groups']
        self.url_groups_detail = self.endpoints['groups-detail']

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

    def test_api_user_get_is_not_public(self):
        """
        Test api user endpoint with GET method is not public
        Anonymous user can not list user
        """
        super().status_code_is(
                'GET', self.url_users, None, status.HTTP_401_UNAUTHORIZED
                )

    def test_api_group_get_is_not_public(self):
        """
        Test api group endpoint with GET method is not public
        Anonymous user can not list group
        """
        super().status_code_is(
                'GET', self.url_groups, None, status.HTTP_401_UNAUTHORIZED)

    def test_api_user_post_is_public(self):
        """
        Test api user endpoint with POST method is public
        Anonymous user can create an account
        """
        data = {'username': 'gate', 'password': 'steve',
                'email': 'steve@gate.org'
                }
        super().status_code_is(
                'POST', self.url_users, data, status.HTTP_201_CREATED)

    def test_api_group_post_is_not_public(self):
        """
        Test api group endpoint with POST method is not public
        Anonymous user cannot create a group
        """
        data = {'name': 'user-group'}
        super().status_code_is(
                'POST', self.url_groups, data, status.HTTP_401_UNAUTHORIZED)

    def test_api_user_detail_get_is_not_public(self):
        """
        Test api user detail endpoint with GET method is not public
        Anonymous user can not retrieve user information
        """
        super().status_code_is(
                'GET', self.url_users_detail, None,
                status.HTTP_401_UNAUTHORIZED
                )

    def test_api_group_detail_get_is_not_public(self):
        """
        Test api group detail endpoint with GET method is not public
        Anonymous user can not retrieve group information
        """
        super().status_code_is(
                'GET', self.url_groups_detail, None,
                status.HTTP_401_UNAUTHORIZED
                )

    def test_api_user_detail_put_is_not_public(self):
        """
        Test api user detail endpoint with PUT method is not public
        Anonymous user can not update a user instance
        """
        data = {'password': 'inject'}
        super().status_code_is(
                'PUT', self.url_users_detail, None,
                status.HTTP_401_UNAUTHORIZED
                )

    def test_api_group_detail_put_is_not_public(self):
        """
        Test api group detail endpoint with PUT method is not public
        Anonymous user can not update a group instance
        """
        data = {'name': 'new-group-name'}
        super().status_code_is(
                'PUT', self.url_groups_detail, None,
                status.HTTP_401_UNAUTHORIZED
                )

    def test_api_user_detail_delete_is_not_public(self):
        """
        Test api user detail endpoint with DELETE method is not public
        Anonymous user can not delete an user instance
        """
        super().status_code_is(
                'DELETE', self.url_users_detail, None,
                status.HTTP_401_UNAUTHORIZED
                )

    def test_api_group_detail_delete_is_not_public(self):
        """
        Test api group detail endpoint with DELETE method is not public
        Anonymous user can not delete a group instance
        """
        super().status_code_is(
                'DELETE', self.url_groups_detail, None,
                status.HTTP_401_UNAUTHORIZED
                )

class APIUserPermission(GenericAPIStatusCode):
    """
    Test API user level permission to endpoints
    """

    def setUp(self):
        super().setUp()
        super().force_authenticate(self.user)
        self.url_users = self.endpoints['users']
        self.url_users_detail = self.endpoints['users-detail']
        self.url_groups = self.endpoints['groups']
        self.url_groups_detail = self.endpoints['groups-detail']

    def test_api_user_get_is_forbidden(self):
        """
        Test api user endpoint with GET method is forbidden for user
        User can not list user
        """
        super().status_code_is(
                'GET', self.url_users, None, status.HTTP_403_FORBIDDEN)

    def test_api_group_get_is_accessible(self):
        """
        Test api group endpoint with GET method is accessible
        User can list his own groups
        """
        super().status_code_is(
                'GET', self.url_groups, None, status.HTTP_200_OK)

    def test_api_user_post_is_public(self):
        """
        Test api user endpoint with POST method is accessible
        User can create another account
        """
        data = {'username': 'gate', 'password': 'steve',
                'email': 'steve@gate.org'
                }
        super().status_code_is(
                'POST', self.url_users, data, status.HTTP_201_CREATED)

    def test_api_group_post_is_forbidden(self):
        """
        Test api group endpoint with POST method is forbidden
        User cannot create a group
        """
        data = {'name': 'user-group'}
        super().status_code_is(
                'POST', self.url_groups, data, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_get_is_ok(self):
        """
        Test api user detail endpoint with GET method is ok
        User can retrieve his own information
        """
        url = reverse('users-detail-api', args=(2,))
        super().status_code_is(
                'GET', url, None, status.HTTP_200_OK)

    def test_api_group_detail_get_is_ok(self):
        """
        Test api group detail endpoint with GET method is ok
        User can retrieve his own group information
        """
        url = reverse('groups-detail-api', args=(1,))
        super().status_code_is(
                'GET', url, None, status.HTTP_200_OK)

    def test_api_user_detail_get_other_user_is_forbidden(self):
        """
        Test api user detail endpoint with GET method is forbidden for user
        User can not retrieves other user information
        """
        super().status_code_is(
                'GET', self.url_users_detail, None,
                status.HTTP_403_FORBIDDEN)

    def test_api_group_detail_get_other_group_is_forbidden(self):
        """
        Test api group detail endpoint with GET method is forbidden for user
        User can not retrieve group information that he is not a member
        """
        url = reverse('groups-detail-api', args=(2,))
        super().status_code_is('GET', url, None, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_put_is_ok(self):
        """
        Test api user detail endpoint with POST method is ok
        User can update his user instance
        """
        url = reverse('users-detail-api', args=(2,))
        data = {'password': 'inject'}
        super().status_code_is(
                'PUT', url, data, status.HTTP_200_OK)

    def test_api_group_detail_put_is_forbidden(self):
        """
        Test api group detail endpoint with PUT method is forbidden
        User can not update group instance
        """
        data = {'name': 'change-group'}
        super().status_code_is(
                'PUT', self.url_groups_detail, data, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_put_other_user_is_forbidden(self):
        """
        Test api user detail endpoint with POST method is forbidden
        User can not update other user instance
        """
        url = reverse('users-detail-api', args=(3,))
        data = {'password': 'inject'}
        super().status_code_is(
                'PUT', url, data, status.HTTP_403_FORBIDDEN)

    def test_api_user_detail_delete_is_ok(self):
        """
        Test api user detail endpoint with DELETE method is ok
        User can delete his user instance
        """
        url = reverse('users-detail-api', args=(2,))
        super().status_code_is(
                'DELETE', url, None, status.HTTP_204_NO_CONTENT)

    def test_api_user_detail_delete_other_user_is_forbidden(self):
        """
        Test api user detail endpoint with DELETE method is forbidden
        User can not delete other user instance
        """
        url = reverse('users-detail-api', args=(3,))
        super().status_code_is(
                'DELETE', url, None, status.HTTP_403_FORBIDDEN)

class APIAdminPermission(GenericAPIStatusCode):
    """
    Test API admin level permission to endpoints
    """

    def setUp(self):
        super().setUp()
        super().force_authenticate(self.admin)
        self.url_users = self.endpoints['users']
        self.url_users_detail = self.endpoints['users-detail']
        self.url_groups = self.endpoints['groups']

    def test_api_user_get_is_accessible(self):
        """
        Test api user endpoint with GET method is accessible by admin
        An admin can list user
        """
        super().status_code_is(
                'GET', self.url_users, None, status.HTTP_200_OK)

    def test_api_group_get_is_accessible(self):
        """
        Test api group endpoint with GET method is accessible by admin
        An admin can list user
        """
        super().status_code_is(
                'GET', self.url_groups, None, status.HTTP_200_OK)

    def test_api_user_post_is_accessible(self):
        """
        Test api user endpoint with POST method is accessible by admin
        An admin can create a user
        """
        data = {'username': 'foo', 'password': 'bar', 'email': 'foo@bar.foo'}
        super().status_code_is(
                'POST', self.url_users, data, status.HTTP_201_CREATED)

    def test_api_group_post_is_accessible(self):
        """
        Test api group endpoint with POST method is accessible by admin
        An admin can create a group
        """
        data = {'name': 'foo'}
        super().status_code_is(
                'POST', self.url_groups, data, status.HTTP_201_CREATED)

    def test_api_user_detail_get_is_accessible(self):
        """
        Test api user detail endpoint with GET method is accessible by admin
        Admin can access user instance information
        """
        url = reverse('users-detail-api', args=(2,))
        super().status_code_is(
                'GET', self.url_users_detail, None, status.HTTP_200_OK)

    def test_api_user_detail_put_is_accessible(self):
        """
        Test api user detail endpoint with PUT method is accessible by admin
        Admin can update user instance
        """
        url = reverse('users-detail-api', args=(2,))
        data = {'firstname': 'foobar'}
        super().status_code_is(
                'PUT', url, data, status.HTTP_200_OK)

    def test_api_user_detail_put_is_accessible(self):
        """
        Test api user detail endpoint with DELETE method is accessible by admin
        Admin can delete a user instance
        """
        url = reverse('users-detail-api', args=(2,))
        super().status_code_is(
                'DELETE', url, None, status.HTTP_204_NO_CONTENT)
