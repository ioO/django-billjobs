from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^generate_pdf/(?P<bill_id>\d+)$', views.generate_pdf,
        name='generate-pdf'),
    url(r'^users/$', views.UserAdmin.as_view(), name='users'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserAdminDetail.as_view(), name='user-detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]
