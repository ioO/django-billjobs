import csv
from django import forms
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.urlresolvers import reverse
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from .models import Bill, BillLine, Service, UserProfile

class BillLineInlineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BillLineInlineForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['service'].queryset = Service.objects.filter(Q(is_available=True) | Q(name=self.instance.service.name))
            print(self.fields['service'].choices)
        else:
            self.fields['service'].queryset = Service.objects.filter(is_available=True)

    class Meta:
        model = BillLine
        fields = ('service', 'quantity', 'total', 'note')

class BillLineInline(admin.TabularInline):
    model = BillLine
    extra = 1
    form = BillLineInlineForm


class BillAdmin(admin.ModelAdmin):
    readonly_fields = ('number', 'billing_date', 'amount')
    exclude = ('issuer_address', 'billing_address')
    inlines = [BillLineInline]
    list_display = ('__str__', 'coworker_name_link', 'amount', 'billing_date',
            'isPaid', 'pdf_file_url')
    list_editable = ('isPaid',)
    list_filter = ('isPaid', )
    search_fields = ('user__first_name', 'user__last_name', 'number', 'amount')

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(BillAdmin, self).formfield_for_foreignkey(
                                                db_field, request, **kwargs)
        if db_field.rel.to == User:
            field.initial = request.user.id
            field.label_from_instance = self.get_user_label
        return field

    def get_user_label(self, user):
        name = user.get_full_name()
        username = user.username
        return (name and name != username and '%s (%s)' % (name, username)
                or username)

    def coworker_name_link(self, obj):
        ''' Create a link to user admin edit view '''
        return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:auth_user_change', args=(obj.user.id,)),
                obj.coworker_name())
    coworker_name_link.short_description = _('Coworker name')

    def pdf_file_url(self, obj):
        return format_html(
                '<a href="{}">{}.pdf</a>',
                reverse('generate-pdf', args=(obj.id,)),
                obj.number)
    pdf_file_url.short_description=_('Download invoice')

class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

class UserProfileAdmin(admin.StackedInline):
    model = UserProfile
    formset = RequiredInlineFormSet

class UserForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

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
    actions = ['export_email']
    form = UserForm

    def export_email(self, request, queryset):
        """ Export emails of selected account """
        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        for email in queryset.values_list('email'):
            writer.writerow(email)

        return response
    export_email.short_description = _('Export email of selected users')

class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ('__str__', 'price', 'is_available')
    list_editable = ('is_available',)
    list_filter = ('is_available',)

admin.site.register(Bill, BillAdmin)
admin.site.register(Service, ServiceAdmin)

# User have to be unregistered
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
