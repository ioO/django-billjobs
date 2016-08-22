# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 23:41
from __future__ import unicode_literals

from django.db import migrations

def add_billing_address(apps, schema_editor):
    ''' Data migration add billing_address in Bill from user billing_address 
    field
    '''
    Bill = apps.get_model('billjobs', 'Bill')
    for bill in Bill.objects.all():
        bill.billing_address = bill.user.billing_address
        bill.save()

class Migration(migrations.Migration):

    dependencies = [
        ('billjobs', '0002_service_is_available_squashed_0005_bill_issuer_address_default'),
    ]

    operations = [
        migrations.RunPython(add_billing_address),
    ]
