from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from billing.models import Bill, BillLine, Service, UserProfile

class BillLineInline(admin.TabularInline):
    model = BillLine
    extra = 1

class BillAdmin(admin.ModelAdmin):
    inlines = [BillLineInline]

class UserProfileAdmin(admin.StackedInline):
    model = UserProfile

class UserAdmin(UserAdmin):
    inlines = (UserProfileAdmin, )

admin.site.register(Bill, BillAdmin)
admin.site.register(Service)

# User have to be unregistered
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
