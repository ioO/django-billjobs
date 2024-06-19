========
Billjobs
========
.. image:: https://travis-ci.org/ioO/django-billjobs.svg?branch=master
   :alt: Travis Build Status
   :target: https://travis-ci.org/ioO/django-billjobs

.. image:: https://coveralls.io/repos/github/ioO/django-billjobs/badge.svg?branch=master
   :target: https://coveralls.io/github/ioO/django-billjobs?branch=master
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-billjobs/badge/?version=latest
   :target: http://django-billjobs.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

**Warning: I maintain this project 2/3 times a year.** If you start a new coworking space as a french non-profit
organization, this project could help you on the first time. Otherwise, it must be wiser to use another software.

A django billing app for coworking space.

We intend to keep things as simple as we can and with an easy user experience. This apps is designed to manage invoices
of coworkers.

**No tax management**. There is no tax for non-profit organization in
France. This application doesn't manage tax, it displays only legal
French informations and tax 0% in invoice.

We use it at `Cowork'in Montpellier <http://www.coworkinmontpellier.org>`__ and `Le Vîllage <https://www.levillage.co/>`__, 
two coworking spaces in South of France

  * `Documentation <http://django-billjobs.readthedocs.io/en/latest/>`__
  * `Issue Tracking <https://github.com/ioO/django-billjobs/issues>`__

Upgrade dependencies
--------------------
``
pipenv install
pipenv requirements > requirements.txt
``

How to release
--------------
``
rm -rf dist/*
pipenv run python3 -m build
pipenv run twine upload dist/*
``
More information: https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
