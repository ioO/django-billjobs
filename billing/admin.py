from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from billing.models import Bill, BillLine, Service, UserProfile

class BillLineInline(admin.TabularInline):
    model = BillLine
    extra = 1

class BillAdmin(admin.ModelAdmin):
    inlines = [BillLineInline]
    list_display = ('__unicode__', 'coworker_name', 'amount', 'billing_date', 
            'isPaid', 'pdf_file_url')
    list_editable = ('isPaid',)

    def pdf_file_url(self, obj):
        return '<a href="%s">%s.pdf</a>' % (reverse('generate_pdf', 
            args=(obj.id,)), obj.number)

    pdf_file_url.allow_tags = True


class UserProfileAdmin(admin.StackedInline):
    model = UserProfile

class UserAdmin(UserAdmin):
    inlines = (UserProfileAdmin, )
    fieldsets = (
            (None, {
                'fields': ('username', 'password')
                }),
            (_('Personal info'), {
                'fields': ('first_name', 'last_name', 'email')
                }),
            (_('Permissions'), {
                'classes': ('collapse',),
                'fields': ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
                }),
            (_('Important dates'), {
                'classes': ('collapse',),
                'fields': ('last_login', 'date_joined')
                })
            )
    list_display = ('username', 'get_full_name', 'email')

class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ('__unicode__', 'price')

admin.site.register(Bill, BillAdmin)
admin.site.register(Service, ServiceAdmin)

# User have to be unregistered
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
