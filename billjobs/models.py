from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete
# TODO delete this import
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from .settings import BILLJOBS_BILL_ISSUER
import datetime


@python_2_unicode_compatible
class Bill(models.Model):

    user = models.ForeignKey(User, verbose_name=_('Coworker'))
    number = models.CharField(max_length=10, unique=True, blank=True, 
            verbose_name=_('Bill number'),
            help_text=_('This value is set automatically.'))
    isPaid = models.BooleanField(default=False, 
            verbose_name=_('Bill is paid ?'),
            help_text=_('Check this value when bill is paid'))
    billing_date = models.DateField(auto_now_add=True,verbose_name=_('Date'),
            help_text=_('This value is set automatically.'))
    amount = models.FloatField(blank=True, default=0, 
            verbose_name=_('Bill total amount'),
            help_text=_('The amount is computed automatically.'))
    issuer_address = models.CharField(max_length=1024, blank=False, 
            default=BILLJOBS_BILL_ISSUER)
    billing_address = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        return self.number

    def coworker_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    coworker_name.short_description = _('Coworker name')

    class Meta:
        verbose_name = _('Bill')

    def save(self, *args, **kwargs):
        if not self.billing_address:
            self.billing_address = self.user.userprofile.billing_address
        super(Bill,self).save(*args,**kwargs)


@python_2_unicode_compatible
class Service(models.Model):

    reference = models.CharField(max_length=5, verbose_name=_('Reference'))
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    description = models.CharField(max_length=256,
            verbose_name=_('Description'),
            help_text=_('Write service description limited to 256 characters'))
    price = models.FloatField(verbose_name=_('Price'))
    is_available = models.BooleanField(verbose_name=_('Is available ?'),
            default=True)

    def __str__(self):
        """ Return name as object representation """
        return self.name

    class Meta:
        verbose_name = _('Service')

class BillLine(models.Model):

    bill = models.ForeignKey(Bill)
    service = models.ForeignKey(Service)
    quantity = models.SmallIntegerField(default=1, verbose_name=_('Quantity'))
    total = models.FloatField(blank=True,
            help_text=_('This value is computed automatically'), 
            verbose_name=_('Total'))
    note = models.CharField(max_length=1024, verbose_name=_('Note'), 
            blank=True, 
            help_text=_('Write a simple note which will be added in your bill')
            )

    class Meta:
        verbose_name = _('Bill Line')
        verbose_name_plural = _('Bill Lines')

class UserProfile(models.Model):
    """ extend User class """
    user = models.OneToOneField(User)
    billing_address = models.TextField(max_length=1024, 
            verbose_name=_('Billing Address'))

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')


@receiver(pre_save, sender=BillLine)
def compute_total(sender, instance, **kwargs):
        """ set total of line automatically """
        if not instance.total:
            instance.total = instance.service.price * instance.quantity

@receiver(pre_save, sender=Bill)
def define_number(sender, instance, **kwargs):
    """ set bill number incrementally """

    # only when we create record for the first time
    if not instance.number:
        today = datetime.date.today()
        # get last id in base, we assume it's the last record
        try:
            last_record = sender.objects.latest('id')
            #get last bill number and increment it
            last_num = '%03d' % (int(last_record.number[-3:])+1)
        # no Bill in db
        except sender.DoesNotExist:
            last_num = '001'

        instance.number = 'F%s%s' % (today.strftime('%Y%m'), last_num)

@receiver(pre_save, sender=Bill)
def bill_pre_save(sender, instance, **kwargs):
    """ Always compute the total amount of one bill before save. """
    set_bill_amount(sender, instance, **kwargs)

# If you change a BillLine, Bill object is not save, so pre_save do not compute
# the total amount.
@receiver(post_save, sender=BillLine)
@receiver(post_delete, sender=BillLine)
def bill_billLine_post_save_and_delete(sender, instance, **kwargs):
    """ Update Bill total amount when related billLines change 
        When admin modify or delete a BillLine, Bill instance has no change, so
        the pre_save is not called and total amount is not computed.
    """
    set_bill_amount(sender, instance.bill, **kwargs)

def set_bill_amount(sender, instance, **kwargs):
    """ set total price of billing when saving """
    # reset self.amount in case is already set
    bill = instance
    bill.amount = 0
    for line in bill.billline_set.all():
        bill.amount += line.total

    if sender is not Bill:
        bill.save()
