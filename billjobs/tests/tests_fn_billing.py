from django.test import TestCase
from django.contrib.auth.models import User


class BillingAdminListViewTestCase(TestCase):
    ''' Test billing model admin view '''
    fixtures = ['test_billing_admin.yaml']

    def test_coworker_name_link_to_user(self):
        ''' Test link to user view in BillAdmin list view '''
        admin = User.objects.get(pk=1)
        self.client.force_login(admin)
        response = self.client.get('/admin/billjobs/bill/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                '<td class="field-coworker_name_link"><a href="/admin/auth/user/1/change/">Bill Jobs</a></td>')
