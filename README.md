Billjobs
========

A django billing app for coworking space.

This app is designed to manage bills for the coworking space **Cowork'in Montpellier**.
We intend to stay easy and lite. You can manage coworkers informations and their respective bills.

No tax management.  There is no tax for non-profit organization in France. This application doesn't manage tax, it only 
displays legal French informations and tax 0% on bills.

###User and Group

User and Group management is provided by [django auth](https://docs.djangoproject.com/en/dev/topics/auth/) module.

###Billing

Billing application provides two features **bills** and **services**

Bills module allows you to list, create, modify or delete bills. You can generate a pdf and download it.
You can change **services** default price. Total amount of bill is computed automatically after saving. Bill number is 
also set automatically after saving.

Service module allows you to list, create, modify or delete services.

Organisation
------------

Billjobs project uses [git flow](http://nvie.com/posts/a-successful-git-branching-model/)

**develop** branch is for development.
**master** branch contains last release.

Installation
------------

### For development

**Clone repository**

    git clone https://github.com/ioO/billjobs.git

**Checkout develop branch**

    git checkout develop

**Create a virtualenv with python 3 binary**

Billjobs was initially written with __python 2.7__ and move to __python 3.4__

Read [virtualenv documentation](http://virtualenvwrapper.readthedocs.org/en/latest/ "Virtualenv")

    mkvirtualenv billjobs --python=/path/to/python3.4

**Install dependencies**

    pip install -r requirements.txt

**Database**

Development use sqlite3 engine.

    ./manage.py syncdb

If you set a super user it will not work. Read this issue #7

A default super user is in fixtures.
Login : bill
Password : jobs

###For testing

Last stable release is master branch

**Clone repository**

    git clone https://github.com/ioO/billjobs.git

**Create a virtualenv with python 3 binary**

Billjobs was initially written with __python 2.7__ and move to __python 3.4__

Read [virtualenv documentation](http://virtualenvwrapper.readthedocs.org/en/latest/ "Virtualenv")

    mkvirtualenv billjobs --python=/path/to/python3.4

**Install dependencies**

    pip install -r requirements.txt

All development dependencies are removed.

**Database**

Default database settings are sqlite3 engine.

    ./manage.py syncdb

Fixtures with initial data are removed.

Licence
=======

This application is under [MIT License](http://en.wikipedia.org/wiki/MIT_License "MIT License") see *LICENSE.md* file.
