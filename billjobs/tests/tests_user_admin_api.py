from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, \
        force_authenticate
from billjobs.views import UserAdmin, UserAdminDetail
import json

class UserAdminAPIStatusCode(TestCase):
    """
    Test status code returned by endpoints
    Status code related to permission are tested in APIPermission class
    """

    fixtures = ['test_api_user.yaml']

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.url = reverse('user')

    def test_user_admin_get_is_200(self):
        """
        Test api user admin endpoints with GET method is HTTP_200_OK
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_admin_post_is_201(self):
        """
        Test api user admin endpoints with POST method is HTTP_201_CREATED
        """
        data = {'username': 'foo', 'password': 'bar', 'email': 'foo@bar.org'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_admin_post_is_400(self):
        """
        Test api user admin endpoints with POST method is HTTP_400_BAD_REQUEST
        when input data are incorrect
        """
        data = {'username': 'foo'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_admin_put_is_405(self):
        """
        Test api user admin endpoints with PUT return
        HTTP_405_METHOD_NOT_ALLOWED
        """
        data = {'username': 'foo'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_admin_delete_is_405(self):
        """
        Test api user admin endpoints with DELETE return
        HTTP_405_METHOD_NOT_ALLOWED
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED)

class UserAdminDetailAPIStatusCode(TestCase):
    """
    Test user admin detail api response status code
    """

    fixtures=['test_api_user.yaml']

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.url = reverse('user-detail', args=[2])

    def test_user_detail_get_is_200(self):
        """
        Test api user detail endpoints with GET return HTTP_200_OK
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_get_is_404_with_bad_pk(self):
        """
        Test api user detail endpoints with GET return HTTP_404_NOT_FOUND
        when user pk does not exist
        """
        response = self.client.get(reverse('user-detail', args=[1234]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail_put_is_200(self):
        """
        Test api user detail endpoints with PUT method return HTTP_200_OK
        """
        data = {'username': 'foo', 'last_name': 'bar'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_put_is_404_with_bad_pk(self):
        """
        Test api user detail endpoints with PUT return HTTP_404_NOT_FOUND
        when user pk does not exist
        """
        data = {'username': 'foo', 'last_name': 'bar'}
        response = self.client.put(reverse('user-detail', args=[1234]), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail_put_is_400_with_wrong_data(self):
        """
        Test api user detail endpoints with PUT return HTTP_400_BAD_REQUEST
        with wrong data in json (here username already exists)
        """
        data = {'username': 'bill', 'last_name': 'bar',
                'not_a_field': 'hello'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAdminAPI(TestCase):
    """ Test User Admin API REST endpoint """

    fixtures=['test_api_user.yaml']

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

    def test_admin_update_user(self):
        data = {'username': 'bill'}
        self.client.force_authenticate(user=self.admin)
        response = self.client.put('/billjobs/users/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_delete_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete('/billjobs/users/3/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
