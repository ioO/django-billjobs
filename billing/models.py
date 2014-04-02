from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, pre_init
import datetime


class Bill(models.Model):

    number = models.CharField(max_length=10, unique=True, blank=True)
    isPaid = models.BooleanField(default=False)
    billing_date = models.DateField()


class Service(models.Model):

    reference = models.CharField(max_length=5)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    price = models.FloatField()

    def __unicode__(self):
        """ Return name as object representation """
        return self.name


class BillLine(models.Model):

    bill = models.ForeignKey(Bill)
    service = models.ForeignKey(Service)
    quantity = models.SmallIntegerField(default=1)
    total = models.FloatField(blank=True)


class UserProfile(models.Model):
    """ extend User class """
    user = models.OneToOneField(User)
    billing_address = models.CharField(max_length=1024)


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
