# Generated by Django 3.2.15 on 2023-11-17 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billjobs', '0009_auto_20190114_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, help_text='This value is set automatically.', max_length=16, unique=True, verbose_name='Quote number')),
                ('creation_date', models.DateField(auto_now_add=True, help_text='This value is set automatically.', verbose_name='Date')),
                ('expiration_date', models.DateField(help_text='This value is set automatically.', verbose_name='Date')),
                ('amount', models.FloatField(blank=True, default=0, help_text='The amount is computed automatically.', verbose_name='Bill total amount')),
                ('issuer_address', models.CharField(default='\n            Your Coworking Space Name<br/>Building name<br/>\n            Number & Street<br/>Postal Code Town\n            ', max_length=1024)),
                ('billing_address', models.CharField(blank=True, max_length=1024)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Coworker')),
            ],
        ),
        migrations.CreateModel(
            name='QuoteLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(default=1, verbose_name='Quantity')),
                ('total', models.FloatField(blank=True, help_text='This value is computed automatically', verbose_name='Total')),
                ('note', models.CharField(blank=True, help_text='Write a simple note which will be added in your quote', max_length=1024, verbose_name='Note')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='billjobs.quote')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='billjobs.service')),
            ],
            options={
                'verbose_name': 'Quote Line',
                'verbose_name_plural': 'Quote Lines',
            },
        ),
    ]
