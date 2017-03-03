from django.test import TestCase, Client
from django.contrib.auth.models import User
from billjobs.models import Bill, UserProfile

class BillingAdminListViewTestCase(TestCase):
    ''' Test billing model admin view '''

    def test_coworker_name_link_to_user(self):
        admin = User.objects.create_superuser(
                username='admin', password='123', email='admin@billjobs.org',
                first_name = 'Bill', last_name = 'Jobs')
        profile = UserProfile(user=admin, billing_address='street')
        profile.save()
        invoice = Bill()
        invoice.user = admin
        invoice.save()
        self.client.force_login(admin)
        response = self.client.get('/admin/billjobs/bill/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                '<td class="field-coworker_name_link"><a href="/admin/auth/user/1/change/">Bill Jobs</a></td>')
