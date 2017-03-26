from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, \
        force_authenticate
from billjobs.views import UserAdmin, UserAdminDetail
import json

class UserAdminAPI(TestCase):
    """ Test User Admin API REST endpoint """

    fixtures=['account_test.yaml']

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.admin = User.objects.get(pk=1)
        self.user = User.objects.get(pk=2)

    def test_admin_list_user(self):
        request = self.factory.get('/billjobs/users/')
        force_authenticate(request, user=self.admin)
        view = UserAdmin.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_retrieve_user(self):
        request = self.factory.get('/billjobs/users/')
        force_authenticate(request, user=self.admin)
        view = UserAdminDetail.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_404_if_no_user_pk(self):
        request = self.factory.get('/billjobs/users')
        force_authenticate(request, user=self.admin)
        view = UserAdminDetail.as_view()
        response = view(request, pk=123)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_do_not_list_user(self):
        request = self.factory.get('/billjobs/users/')
        view = UserAdmin.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_do_not_retrieve_user(self):
        request = self.factory.get('/billjobs/users/')
        view = UserAdmin.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_do_not_list_user(self):
        request = self.factory.get('/billjobs/users/')
        force_authenticate(request, user=self.user)
        view = UserAdmin.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_do_not_retrieve_user(self):
        request = self.factory.get('/billjobs/users/')
        force_authenticate(request, user=self.user)
        view = UserAdminDetail.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_user(self):
        request = self.factory.post('/billjobs/users/',
                json.dumps({
                    'username': 'new_user',
                    'email': 'new@jobs.org',
                    'password': 'foobar'}),
                content_type='application/json')
        force_authenticate(request, user=self.admin)
        view = UserAdmin.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_create_user_get_400(self):
        request = self.factory.post('/billjobs/users/',
                json.dumps({
                    'email': 'new@jobs.org',
                    'password': 'foobar'}),
                content_type='application/json')
        force_authenticate(request, user=self.admin)
        view = UserAdmin.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_not_create_user(self):
        request = self.factory.post('/billjobs/users/',
                json.dumps({
                    'username': 'new_user',
                    'email': 'new@jobs.org',
                    'password': 'foobar'}),
                content_type='application/json')
        force_authenticate(request, user=self.user)
        view = UserAdmin.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_can_not_create_user(self):
        request = self.factory.post('/billjobs/users/',
                json.dumps({
                    'username': 'new_user',
                    'email': 'new@jobs.org',
                    'password': 'foobar'}),
                content_type='application/json')
        view = UserAdmin.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_update_user(self):
        data = {'username': 'bill'}
        self.client.force_authenticate(user=self.admin)
        response = self.client.put('/billjobs/users/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_auth_token(self):
        data = {'username': self.admin.username, 'password': 'jobs'}
        response = self.client.post('/billjobs/api-token-auth/', data,
                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_delete_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete('/billjobs/users/3/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
