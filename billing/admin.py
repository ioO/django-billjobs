from django.contrib import admin
from billing.models import Bill, BillLine

admin.site.register(Bill)
admin.site.register(BillLine)
