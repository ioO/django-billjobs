from django.conf.urls import include, url
from django.contrib import admin
admin.site.site_header = 'Coworking space administration'

urlpatterns = [
    url(r'^billing/', include('billing.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
