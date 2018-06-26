from django.conf.urls import include, url
from core import settings
from billjobs.admin import admin_site
admin_site.site_header = 'Coworking space administration'

urlpatterns = [
    url(r'^billjobs/', include('billjobs.urls')),
    url(r'^admin/', include(admin_site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
