===============
Getting Started
===============

`Django-billjobs`_ is a Django reusable app that you can install with `pip`_. We recommend you follow those steps to 
setup a new project for your coworking space :

Create virtualenv
-----------------
You need Python version 3.5 at least, `virtualenv`_ and `mkvirtualenv`_ installed in your system. We let you read 
their own respective documentation. Let's create a virtualenv with your coworking space name

.. code-block:: bash

    [ioo@billjobs ~/]$ mkvirtualenv my-space-name
    Using base prefix '/usr'
    New python executable in ~/.virtualenv/my-space-name/bin/python3
    Also creating executable in ~/.virtualenv/my-space-name/bin/python
    Installing setuptools, pip, wheel...done.
    virtualenvwrapper.user_scripts creating ~/.virtualenv/my-space-name/bin/predeactivate
    virtualenvwrapper.user_scripts creating ~/.virtualenv/my-space-name/bin/postdeactivate
    virtualenvwrapper.user_scripts creating ~/.virtualenv/my-space-name/bin/preactivate
    virtualenvwrapper.user_scripts creating ~/.virtualenv/my-space-name/bin/postactivate
    virtualenvwrapper.user_scripts creating ~/.virtualenv/my-space-name/bin/get_env_details

    (my-space-name) [ioo@billjobs ~/django-billjobs]$

Everything is ok, your virtualenv should be activated as you can see above with the name between parenthesis.

Install Django-billjobs
-----------------------

Most of the time, Django-billjobs is up to date with the latest Django version. You can check which version we actually 
support in the `travis.yml`_ file. You can install Django-billjobs directly, all requirements as Django, reportlab and 
Django REST Framework will be installed in the same time.

.. code-block:: bash

    (my-space-name) [ioo@billjobs ~/my-space-name]$ pip install Django-billjobs
    Collecting Django-billjobs
    Collecting django>1.9 (from Django-billjobs)
      Using cached Django-1.11-py2.py3-none-any.whl
    Collecting djangorestframework==3.6.2 (from Django-billjobs)
      Using cached djangorestframework-3.6.2-py2.py3-none-any.whl
    Collecting reportlab==3.4.0 (from Django-billjobs)
      Using cached reportlab-3.4.0-cp36-cp36m-manylinux1_x86_64.whl
    [...]
    Installing collected packages: pytz, django, djangorestframework, olefile, pillow, reportlab, Django-billjobs
    Successfully installed Django-billjobs-1.0.0 django-1.11 djangorestframework-3.6.2 olefile-0.44 pillow-4.1.0 pytz-2017.2 reportlab-3.4.0



Create your django project
--------------------------

Now everything is installed you can create a django project.

.. code-block:: bash

    (my-space-name) [ioo@billjobs ~/]$ mkdir my-space-name
    (my-space-name) [ioo@billjobs ~/]$ cd my-space-name/
    (my-space-name) [ioo@billjobs ~/my-space-name]$ django-admin startproject myspacename .
    (my-space-name) [ioo@billjobs ~/my-space-name]$ ls
    manage.py  myspacename

.. note:: You notice the dot at the end of django-admin startproject command, right ? If not you only have a 
  myspacename folder that contains another directory with the same name.

Configure your virtualenv
-------------------------

You need to add the project path to your virtualenv:

.. code-block:: bash

    (my-space-name) [ioo@billjobs ~/my-space-name]$ add2virtualenv .
    Warning: Converting "." to "home/ioo/my-space-name"

Configure the settings path add those lines in postactivate and predeactivate files:

.. code-block:: bash

    # ~/.virtualenv/my-space-name/bin/postactivate
    #!/bin/bash
    # This hook is sourced after this virtualenv is activated.
    export DJANGO_SETTINGS_MODULE=myspacename.settings

.. code-block:: bash

    # ~/.virtualenv/my-space-name/bin/predeactivate
    #!/bin/bash
    # This hook is sourced before this virtualenv is deactivated.
    unset DJANGO_SETTINGS_MODULE

Now deactivate and reactivate the virtualenv to get your changes working.

.. code-block:: bash

    (my-space-name) [ioo@billjobs ~/my-space-name]$ deactivate
    [ioo@billjobs ~/my-space-name]$ workon my-space-name
    (my-space-name) [ioo@billjobs ~/my-space-name]$

Configure your Django project
-----------------------------
You need to enable Django-billjobs in your django project settings, as well as Django REST Framework with the token 
authentification to use the API with your client app.

.. code-block:: python

    # myspacename/settings.py
    INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'billjobs',
    'rest_framework',
    'rest_framework.authtoken',
    )

Django REST Framework allow to browse the API with a web browser. You should configure your project settings to 
allow `SessionAuthentication`_. If you want to use your own application client you should use 
`TokenAuthentication`_. Add those lines in your settings.py

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAdminUser',
            ),
        'PAGE_SIZE': 10
    }

By default, only admin users can access the API. The goal is to avoid to expose sensitives data to public.

Before running and playing with your application, you need to create a database.

.. code-block:: bash

    (my-space-name) [ioo@billjobs ~/my-space-name]$ django-admin migrate
    Operations to perform:
      Apply all migrations: admin, auth, authtoken, billjobs, contenttypes, sessions
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      Applying authtoken.0001_initial... OK
      Applying authtoken.0002_auto_20160226_1747... OK
      Applying billjobs.0001_initial... OK
      Applying billjobs.0002_service_is_available_squashed_0005_bill_issuer_address_default... OK
      Applying billjobs.0006_add_billin_address_and_migrate_data... OK
      Applying billjobs.0007_change_service_description_field_max_len... OK
      Applying sessions.0001_initial... OK

The database is empty, so you need to create a first user with admin permissions to access the backend.

.. code-block:: bash

    (my-space-name) [ioo@billjobs ~/my-space-name]$ django-admin createsuperuser
    Username (leave blank to use 'ioo'): admin
    Email address: admin@billjobs.org
    Password: 
    Password (again): 
    Superuser created successfully.

Last, you need to include *billjobs.urls* to browse the application with your web browser.

.. code-block:: python

    # myspacename/urls.py
    from django.conf.urls import url, include
    from django.contrib import admin

    urlpatterns = [
        url(r'^billjobs/', include('billjobs.urls')),
        url(r'^admin/', admin.site.urls),
    ]

Now you can run the local server and play with django-billjobs

.. code-block:: bash

    (my-space-name) [ioo@billjobs ~/my-space-name]$django-admin runserver
    Performing system checks...
    System check identified no issues (0 silenced).
    April 24, 2017 - 15:46:07
    Django version 1.11, using settings 'myspacename.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

To browse the admin interface http://localhost:8000/admin and to browse the API 
http://localhost:8000/billjobs/api/1.0/users/

.. _Django-billjobs: https://github.com/ioO/django-billjobs/
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _mkvirtualenv: http://virtualenvwrapper.readthedocs.io/en/latest/
.. _Python: https://www.python.org/
.. _pip: https://pypi.python.org/pypi
.. _travis.yml: https://github.com/ioO/django-billjobs/blob/master/.travis.yml
.. _SessionAuthentication: http://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication
.. _TokenAuthentication: http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
