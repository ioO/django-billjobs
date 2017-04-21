Contributing
------------

Clone repository
~~~~~~~~~~~~~~~~

.. code:: shell

    git clone https://github.com/ioO/billjobs.git

Create a virtualenv with python 3 binary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Billjobs works from **python 3.4 to 3.6**.

Read `virtualenv
documentation <http://virtualenvwrapper.readthedocs.org/en/latest/>`__

.. code:: shell

    mkvirtualenv django-billjobs --python=/path/to/python3.5
    add2virtualenv path/to/django-billjobs

Install dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    pip install -r requirements.txt

Sample settings
~~~~~~~~~~~~~~~

The *core/* folder contains sample settings for development. Use
**DJANGO\_SETTINGS\_MODULE** environment variables.

In your virtualenv *bin/postactivate*

.. code:: shell

    export DJANGO_SETTINGS_MODULE=core.settings

In your virtualenv *bin/postdeactivate*

.. code:: shell

    unset DJANGO_SETTINGS_MODULE

Database
~~~~~~~~

Development use sqlite3 engine.

.. code:: shell

    django-admin migrate

Git workflow
~~~~~~~~~~~~

Create a feature branch when you develop a new feature, a hotfix and at
the end rebase it with **master** branch.

.. code:: shell

    git checkout -b new_feature
    # do your commits
    git checkout master
    git pull
    git checkout new_feature
    git rebase master
    git checkout master
    git merge --no-ff new_feature

Fixtures
~~~~~~~~

You can use development fixtures

.. code:: shell

    django-admin loaddata billjobs/fixtures/dev_*

If you setup a super user it will be deleted by fixtures data.

  - Login : bill
  - Password : jobs
