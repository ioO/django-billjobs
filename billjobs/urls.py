from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

api_patterns = [
        url(r'^auth/',
            include('rest_framework.urls', namespace='rest_framework')),
        url(r'^token-auth/', obtain_auth_token, name='api-token-auth'),
        url(r'^users/$', views.UserAPI.as_view(), name='users-api'),
        url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailAPI.as_view(),
            name='users-detail-api'),
        ]

urlpatterns = [
        url(r'api/1.0/', include(api_patterns)),
        url(r'^generate_pdf/(?P<bill_id>\d+)$', views.generate_pdf,
            name='generate-pdf'),
        ]
