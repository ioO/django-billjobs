from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Bill(models.Model):

    bill_date = models.DateField()


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


@receiver(pre_save, sender=BillLine)
def compute_total(sender, instance, **kwargs):
        """ set total of line automatically """
        if not instance.total:
            instance.total = instance.service.price * instance.quantity
