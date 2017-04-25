from django.conf.urls import include, url
from django.contrib import admin
from core import settings
admin.site.site_header = 'Coworking space administration'

urlpatterns = [
    url(r'^billjobs/', include('billjobs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
