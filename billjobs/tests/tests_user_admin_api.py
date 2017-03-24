from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, \
        force_authenticate
from billjobs.views import UserAdmin, UserAdminDetail

class UserAdminAPI(TestCase):
    """ Test User Admin API REST endpoint """

    fixtures=['account_test.yaml']

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.admin = User.objects.get(pk=1)

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

    def test_anonymous_do_not_list_user(self):
        request = self.factory.get('/billjobs/users/')
        view = UserAdmin.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
