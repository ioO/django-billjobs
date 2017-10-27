from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from billjobs.models import Bill, Service
from billjobs.settings import BILLJOBS_BILL_ISSUER


class BillingTestCase(TestCase):
    ''' Test billing creation and modification '''
    fixtures = ['dev_model_010_user.yaml', 'dev_model_020_userprofile.yaml']

    def setUp(self):
        self.user = User.objects.get(username='bill')

    def test_create_bill(self):
        bill = Bill(user=self.user)
        bill.save()
        self.assertEqual(bill.user.username, self.user.username)
        self.assertEqual(bill.issuer_address, BILLJOBS_BILL_ISSUER)
        self.assertEqual(
                bill.billing_address, self.user.userprofile.billing_address)

    def test_user_change_billing_address(self):
        ''' Test when user is changing is billing address
            Previous bill is with old address
            New bill is with new address
        '''
        bill = Bill(user=self.user)
        previous_billing_address = self.user.userprofile.billing_address
        bill.save()
        # user change billing_address
        self.user.userprofile.billing_address = '1 new street\n34000 Town'
        self.user.save()
        new_billing_address = self.user.userprofile.billing_address
        # user create a new bill
        new_bill = Bill(user=self.user)
        new_bill.save()
        self.assertEqual(bill.billing_address, previous_billing_address)
        self.assertEqual(new_bill.billing_address, new_billing_address)

    def test_save_bill_do_not_change_billing_address(self):
        ''' Test when user change his billing address and modify an old bill
            it doesn't change the billing address
        '''
        bill = Bill(user=self.user)
        previous_billing_address = self.user.userprofile.billing_address
        bill.save()
        # user change billing_address
        self.user.userprofile.billing_address = '1 new street\n34000 Town'
        self.user.save()
        # bill is changing
        bill.amount = 100
        bill.save()
        self.assertEqual(bill.billing_address, previous_billing_address)


class ServiceTestCase(TestCase):
    ''' Test CRUD for Service model '''

    def test_create_service_without_price_raise_constraint(self):
        service = Service()
        service.reference = 'TEST'
        service.name = 'Service test'
        with self.assertRaises(IntegrityError):
            service.save()
