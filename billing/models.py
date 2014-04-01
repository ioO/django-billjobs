from django.db import models

class Bill(models.Model):

    bill_date = models.DateField(auto_now_add=True)
    line = models.ForeignKey('BillLine')

class BillLine(models.Model):

     SERVICES_CHOICES = (
            (FT, 'Full Time'),
            (PT, 'Part Time'),
            (MD, 'Mid Time'),
            )

    service = models.CharField(max_length=2, choices=SERVICES_CHOICES, 
                               default=Full Time)
    quantity = models.SmallIntegerField()

