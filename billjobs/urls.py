from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    url(r'^generate_pdf/(?P<bill_id>\d+)$', views.generate_pdf,
        name='generate-pdf'),
    url(r'^user/$', views.UserAdmin.as_view(), name='user'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserAdminDetail.as_view(),
        name='user-detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token, name='api-token-auth')
    ]
