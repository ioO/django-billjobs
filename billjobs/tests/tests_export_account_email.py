from django.test import TestCase
from billjobs.admin import UserAdmin

class EmailExportTestCase(TestCase):
    """ Tests for email account export """

    def test_action_is_avaible(self):
        """ Test admin can select the action in dropdown list """
        self.assertTrue(hasattr(UserAdmin, 'export_email'))
