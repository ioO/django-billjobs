from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from .models import Bill, BillLine, Service, UserProfile

class BillLineInline(admin.TabularInline):
    model = BillLine
    extra = 1

class BillAdmin(admin.ModelAdmin):
    readonly_fields = ('number', 'billing_date', 'amount')
    inlines = [BillLineInline]
    list_display = ('__unicode__', 'coworker_name', 'amount', 'billing_date', 
            'isPaid', 'pdf_file_url')
    list_editable = ('isPaid',)
    list_filter = ('isPaid', )
    search_fields = ('user__first_name', 'user__last_name', 'number')

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(BillAdmin, self).formfield_for_foreignkey(
                                                db_field, request, **kwargs)
        if db_field.rel.to == User:
            field.label_from_instance = self.get_user_label
        return field

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(BillAdmin, self).formfield_for_manytomany(
                                                db_field, request, **kwargs)
        if db_field.rel.to == User:
            field.label_from_instance = self.get_user_label
        return field

    def get_user_label(self, user):
        name = user.get_full_name()
        username = user.username
        return (name and name != username and '%s (%s)' % (name, username)
                or username)

    def pdf_file_url(self, obj):
        return '<a href="%s">%s.pdf</a>' % (reverse('generate-pdf', 
            kwargs={'bill_id': obj.id}), obj.number)

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
