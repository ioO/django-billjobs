from django.test import TestCase
from django.http import HttpResponse
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from billjobs.admin import UserAdmin

class MockRequest(object):
            pass

class EmailExportTestCase(TestCase):
    """ Tests for email account export """

    def setUp(self):
        self.site = AdminSite()
        self.query_set = User.objects.all()

    def test_method_is_avaible(self):
        """ Test admin can select the action in dropdown list """
        self.assertTrue(hasattr(UserAdmin, 'export_email'))

    def test_method_is_model_admin_action(self):
        """ Test method is an custom action for user admin """
        self.assertTrue('export_email' in UserAdmin.actions)

    def test_action_has_a_short_description(self):
        """ Test method has a short description """
        self.assertEqual(UserAdmin.export_email.short_description, 
                'Export email of selected users')

    def test_action_return_http_response(self):
        user_admin = UserAdmin(User, self.site)
        response = user_admin.export_email(request=MockRequest(), queryset=self.query_set)
        self.assertIsInstance(response, HttpResponse)

    def test_action_return_csv(self):
        user_admin = UserAdmin(User, self.site)
        response = user_admin.export_email(request=MockRequest(), queryset=self.query_set)
        self.assertEqual(response.get('Content-Type'), 'text/csv')
