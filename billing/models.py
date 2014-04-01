from django.db import models

class Bill(models.Model):

    bill_date = models.DateField()

class Service(models.Model):

    reference = models.CharField(max_length=5)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    price = models.FloatField()

class BillLine(models.Model):

    bill = models.ForeignKey(Bill)
    service = models.ForeignKey(Service)
    quantity = models.SmallIntegerField(default=1)
    total = models.FloatField()
