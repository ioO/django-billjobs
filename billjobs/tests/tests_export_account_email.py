import csv
import io
from django.test import TestCase
from django.http import HttpResponse
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from billjobs.admin import UserAdmin

class MockRequest(object):
            pass

class EmailExportTestCase(TestCase):
    """ Tests for email account export """

    fixtures = ['test_api_user.yaml']

    def setUp(self):
        self.site = AdminSite()
        self.query_set = User.objects.all()

    def test_method_is_avaible(self):
        """ Test UserAdmin class has method export_email """
        self.assertTrue(hasattr(UserAdmin, 'export_email'))

    def test_method_is_model_admin_action(self):
        """ Test method is an custom action for user admin """
        self.assertTrue('export_email' in UserAdmin.actions)

    def test_action_has_a_short_description(self):
        """ Test method has a short description """
        self.assertEqual(UserAdmin.export_email.short_description,
                'Export email of selected users')

    def test_action_return_http_response(self):
        """ Test method return an HttpResponse """
        user_admin = UserAdmin(User, self.site)
        response = user_admin.export_email(request=MockRequest(),
                queryset=self.query_set)
        self.assertIsInstance(response, HttpResponse)

    def test_action_return_csv(self):
        """ Test method return text/csv as http response content type """
        user_admin = UserAdmin(User, self.site)
        response = user_admin.export_email(request=MockRequest(),
                queryset=self.query_set)
        self.assertEqual(response.get('Content-Type'), 'text/csv')

    def test_action_return_csv_content(self):
        """ Test method return csv content """
        user_admin = UserAdmin(User, self.site)
        response = user_admin.export_email(request=MockRequest(),
                queryset=self.query_set)
        output = io.StringIO()
        writer = csv.writer(output)
        for email in User.objects.values_list('email'):
            writer.writerow(email)
        self.assertEqual(response.content.decode(), output.getvalue())
