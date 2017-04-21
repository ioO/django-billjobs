.. django-billjobs documentation master file, created by
   sphinx-quickstart on Sun Mar 26 14:15:00 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
===========================================
Welcome to django-billjobs's documentation!
===========================================
.. image:: https://travis-ci.org/ioO/django-billjobs.svg?branch=v1.x
   :alt: Travis Build Status
   :target: https://travis-ci.org/ioO/django-billjobs

.. image:: https://readthedocs.org/projects/django-billjobs/badge/?version=latest
:target: http://django-billjobs.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status

*A django billing app for coworking space*

----------
Quickstart
----------

::

    pip install django-billjobs

in your django settings file::

    INSTALLED_APPS = (
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'rest_framework',
      'billjobs',
    )

::

    django-admin migrate
    django-admin createsuperuser
    django-admin runserver

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Features
--------

All the features are managed throught `django
admin.site <https://docs.djangoproject.com/en/1.8/ref/contrib/admin/>`__

-  User and Group management is provided by `django
   auth <https://docs.djangoproject.com/en/dev/topics/auth/>`__ module.
-  Billing management
-  Services management

