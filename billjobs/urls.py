from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^generate_pdf/(?P<bill_id>\d+)$', views.generate_pdf,
        name='generate-pdf'),
    url(r'^users/$', views.UserAdmin.as_view(), name='users'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserAdminDetail.as_view(), name='user-detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token)
    ]
