.. _migration-to-v08x:

====================
Migration to v0.8.x
====================

.. note:: This migration guide concerns all versions before v0.8.0 you update to version v0.8.x or higher

`Django-billjobs`_ version v0.8.x use `Django`_ v2.x version. Some Django functions are removed or going to be
deprecated. You must do some updates in your django project to get the app running.

Settings
--------

Using Django v2.x need changes in your *settings.py* file::

      - MIDDLEWARE_CLASSES=(
      + MIDDLEWARE=(
      -     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',

URLConfs
--------

Django module for url changes. Some functions will be deprecated too::

      -from django.conf.urls import include, url
      +from django.urls import include, path, re_path
       from core import settings
       from billjobs.admin import admin_site
       admin_site.site_header = 'Coworking space administration'

       urlpatterns = [
      -    url(r'^billjobs/', include('billjobs.urls')),
      -    url(r'^admin/', include(admin_site.urls)),
      +    re_path(r'^billjobs/', include('billjobs.urls')),
      +    path('admin/', admin_site.urls),


.. _Django-billjobs: https://github.com/ioO/django-billjobs/
.. _Django: https://djangoproject.com/
