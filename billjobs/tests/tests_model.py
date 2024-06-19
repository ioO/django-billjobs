from django.test import TestCase
from unittest import SkipTest
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from billjobs.models import Bill, Service, Quote
from billjobs.settings import BILLJOBS_BILL_ISSUER
from .factories import ServiceFactory, BillFactory, UserFactory, QuoteFactory
import datetime


class BaseBillingTestCase(TestCase):
    ''' Base testcase class for testing quotes and bills '''
    fixtures = ['dev_model_010_user.yaml', 'dev_model_020_userprofile.yaml']
    target_class = None
    target_factory = None
    document_prefix = ""
    line_set = ""
    abstract = True

    def setUp(self):
        self.user = User.objects.get(username='bill')
        if self.abstract:
            raise SkipTest("This is an abstract class")

    def _line_set(self, obj):
        return getattr(obj, self.line_set)


    def test_create(self):
        bill = self.target_class(user=self.user)
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
        bill = self.target_class(user=self.user)
        previous_billing_address = self.user.userprofile.billing_address
        bill.save()
        # user change billing_address
        self.user.userprofile.billing_address = '1 new street\n34000 Town'
        self.user.save()
        new_billing_address = self.user.userprofile.billing_address
        # user create a new bill
        new_bill = self.target_class(user=self.user)
        new_bill.save()
        self.assertEqual(bill.billing_address, previous_billing_address)
        self.assertEqual(new_bill.billing_address, new_billing_address)

    def test_save_do_not_change_billing_address(self):
        ''' Test when user change his billing address and modify an old bill
            it doesn't change the billing address
        '''
        bill = self.target_class(user=self.user)
        previous_billing_address = self.user.userprofile.billing_address
        bill.save()
        # user change billing_address
        self.user.userprofile.billing_address = '1 new street\n34000 Town'
        self.user.save()
        # bill is changing
        bill.amount = 100
        bill.save()
        self.assertEqual(bill.billing_address, previous_billing_address)

    def test_number_is_more_than_999(self):
        ''' Test the bill number property could be more than 999 '''
        for i in range(1100):
            bill = self.target_class(user=self.user)
            bill.save()
            del(bill)
        # get last bill
        last_bill = self.target_class.objects.order_by('id').last()
        # bills number depend on date, so depend when test is running ;)
        today = datetime.date.today()
        last_number = '%s%s%s' % (self.document_prefix, today.strftime('%Y%m'), '1100')
        self.assertEqual(last_bill.number, last_number)

    def test_service_price_change_do_not_change_bill_line(self):
        '''Test when admin change a service price

        Previous stored bills do not have to be impacted by price change
        '''
        # fixtures
        user = UserFactory()
        # create 4 services and add service to bill
        for i in range(0, 4):
            # create service
            service = ServiceFactory()
            # create bill add service
            bill = self.target_factory(user=user)
            self._line_set(bill).create(service=service)
            # check bill line total is service price
            self.assertEqual(
                    self._line_set(bill).first().total,
                    service.price
                    )
            # update service price
            service.price += 10
            service.save()
            # price is not the same
            self.assertNotEqual(
                    self._line_set(bill).first().total,
                    service.price
                    )

    def test_number_has_no_limit(self):
        ''' Test the object number has no limit '''
        user = UserFactory()
        numbers = (999, 2122, 13456, 123456, 999999)
        # bills number depend on date, so depend when test is running ;)
        prefix = '{}{}'.format(self.document_prefix, datetime.date.today().strftime('%Y%m'))
        for number in numbers:

            # create a bill with forced number
            self.target_factory(user=user, number='{}{}'.format(prefix, number))
            self.target_factory(user=user)
            # get last bill
            last_bill = self.target_class.objects.order_by('id').last()
            # bill number has to be one more
            self.assertEqual(last_bill.number, '{}{}'.format(prefix, number+1))


class BillingTestCase(BaseBillingTestCase):
    ''' TestCase class for testing bills '''
    target_class = Bill
    target_factory = BillFactory
    document_prefix = "F"
    line_set = "billline_set"
    abstract = False


class QuoteTestCase(BaseBillingTestCase):
    ''' TestCase class for testing quotes '''
    target_class = Quote
    target_factory = QuoteFactory
    document_prefix = "D"
    line_set = "quoteline_set"
    abstract = False


class ServiceTestCase(TestCase):
    ''' Test CRUD for Service model '''

    def test_create_service_without_price_raise_constraint(self):
        service = Service()
        service.reference = 'TEST'
        service.name = 'Service test'
        with self.assertRaises(IntegrityError):
            service.save()
