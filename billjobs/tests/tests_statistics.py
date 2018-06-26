from django.test import TestCase
from django.shortcuts import reverse
from billjobs.tests.factories import UserFactory, SuperUserFactory, BillFactory


class Statistics(TestCase):
    '''Tests statistics display page'''

    def setUp(self):
        self.admin = SuperUserFactory()
        self.user = UserFactory()
        self.bill = BillFactory.create(user=self.user)
        self.bill.billing_date = '2018-01-01'
        self.bill.save()

    def test_login_required(self):
        '''Test redirect to admin login page'''
        response = self.client.get('/admin/statistics', follow=True)
        self.assertRedirects(
                response, '/admin/login/?next=/admin/statistics')

    def test_admin_access_stats(self):
        '''Test an authenticated admin can view statistic page'''
        self.client.force_login(self.admin)
        response = self.client.get(
                '/admin/statistics', follow=False)
        self.assertEqual(response.status_code, 200)
