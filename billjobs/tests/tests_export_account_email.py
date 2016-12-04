from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from billjobs.admin import UserAdmin

class EmailExportTestCase(TestCase):
    """ Tests for email account export """

    def test_method_is_avaible(self):
        """ Test admin can select the action in dropdown list """
        self.assertTrue(hasattr(UserAdmin, 'export_email'))

    def test_method_is_model_admin_action(self):
        """ Test method is an custom action for user admin """
        self.assertTrue('export_email' in UserAdmin.actions)
