from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
admin.site.site_header = 'Coworking space administration'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'billjobs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'billing.views.redirect_home'),
    url(r'^admin/generate_pdf/(?P<id>\d+)/$', 'billing.views.generate_pdf', 
        name='generate_pdf'),
    url(r'^admin/', include(admin.site.urls)),
)
