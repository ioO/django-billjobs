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

.. image:: https://coveralls.io/repos/github/ioO/django-billjobs/badge.svg?branch=master
   :target: https://coveralls.io/github/ioO/django-billjobs?branch=master
   :alt: Coverage Status
.
.. image:: https://readthedocs.org/projects/django-billjobs/badge/?version=latest
   :target: http://django-billjobs.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

*A django billing app for coworking space*

-------------------------
What is django-billjobs ?
-------------------------

Django-billjobs_ is a django app to manage coworkers and create their invoices. It uses `Django admin site`_ 
to manage coworkers account, services the space is providing and manage coworkers invoices.

From version `v1.x` Django-billjobs provides an API to let coworking 
spaces develop their own online services for their coworkers based on unique account.

--------
Features
--------

Account and Profile :
  from Django admin site you can create, update, delete coworkers account and their profile. As 
  `Django-billjobs`_ is using `Django authentication system`_ you can also use *groups*.

Services :
  A service can be access to the coworking space for a month, a day, or whatever you want. It is just something
  with a name, a description and a unit price. We keep it simple, really !

Billing :
  You affect one or more services to one account. It creates an invoice and you can download a pdf of it.

.. note:: No tax management.
   This project is coming from non-profit organisation in France. We do not need to manage VAT for services.

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

.. _Django-billjobs: https://github.com/ioO/django-billjobs/
.. _Django admin site: https://docs.djangoproject.com/en/dev/ref/contrib/admin/
.. _v1.x: https://github.com/ioO/django-billjobs/tree/v1.x
.. _Django authentication system: https://docs.djangoproject.com/en/dev/topics/auth/default/
