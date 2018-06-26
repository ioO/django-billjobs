from django.test import TestCase
from django.shortcuts import reverse
from billjobs.tests.factories import UserFactory, BillFactory


class Statistics(TestCase):
    '''Tests statistics display page'''

    def setUp(self):
        self.user = UserFactory()
        self.bill = BillFactory.create(user=self.user)
        self.bill.billing_date = '2018-01-01'
        self.bill.save()

    def test_login_required(self):
        '''Test redirect to admin login page'''
        response = self.client.get(reverse('billjobs_statistics'), follow=True)
        self.assertRedirects(
                response, '/admin/login/?next=/billjobs/statistics/')
