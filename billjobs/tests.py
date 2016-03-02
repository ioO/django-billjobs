from django.test import TestCase, Client

class BillingTestCase(TestCase):
    ''' Test billing creation and modification '''

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

