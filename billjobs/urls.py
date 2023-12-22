from django.urls import path, re_path
from . import views


from .admin import admin_site

urlpatterns = [
        re_path(r'^generate_pdf/(?P<entity_id>\d+)$', views.generate_pdf,
            name='generate-pdf'),
        path('signup/', views.signup, name='billjobs_signup'),
        path('signup-success/', views.signup_success,
            name='billjobs_signup_success'),
        ]
