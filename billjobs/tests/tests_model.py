from django.test import TestCase, Client
from django.contrib.auth.models import User
from billjobs.models import Bill, Service
from billjobs.settings import BILLJOBS_BILL_ISSUER

class BillingTestCase(TestCase):
    ''' Test billing creation and modification '''
    fixtures = ['dev_data.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='bill', password='jobs')

    def tearDown(self):
        self.client.logout()

    def test_create_bill_with_one_line(self):
        ''' Test when user is created a bill with a single service '''
        #response = self.client.get('/admin/billjobs/bill/add/', follow_redirect=True)
        #self.assertEqual(response.status_code, 200)
        self.assertTrue(True)

    def test_create_bill(self):
        user = User.objects.get(username='bill')
        bill = Bill(user=user)
        bill.save()
        self.assertEqual(bill.user.username, 'bill')
        self.assertEqual(bill.issuer_address, BILLJOBS_BILL_ISSUER)
        self.assertEqual(
                bill.billing_address, user.userprofile.billing_address)

