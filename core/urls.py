from django.urls import include, path
from core import settings
from billjobs.admin import admin_site
admin_site.site_header = 'Coworking space administration'

urlpatterns = [
    path('billjobs/', include('billjobs.urls')),
    path('admin/', admin_site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
