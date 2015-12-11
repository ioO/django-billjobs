========
Billjobs
========

A django billing app for coworking space.

This app is designed to manage bills for the coworking space **Cowork'in Montpellier**. We intend to stay easy and 
lite.  You can manage coworkers informations and their respective bills.

**No tax management**. There is no tax for non-profit organization in France. This application doesn't manage tax, it 
only displays legal French informations and tax 0% on bills.

Features
--------

All the features are managed throught [django admin.site](https://docs.djangoproject.com/en/1.8/ref/contrib/admin/)

- User and Group management is provided by [django auth](https://docs.djangoproject.com/en/dev/topics/auth/) module.
- Billing management
- Services management

Installing
----------

    pip install django-billjobs

Contributing
------------

Wow you are awesome ! Thank you.

Git workflow
~~~~~~~~~~~~

Previously we used [git flow](http://nvie.com/posts/a-successful-git-branching-model/)
**develop** branch is here for historical reason

For now I am using a more simple workflow.

Create a feature branch when you develop a new feature, a hotfix and at the end rebase it with **master** branch.

::
  git checkout -b new_feature
  # do your commits
  git checkout master
  git pull
  git rebase master new_feature
  git merge --no-ff new_feature

Release are prefixed by *v*

####Installation

**Clone repository**

    git clone https://github.com/ioO/billjobs.git

**Checkout develop branch**

    git checkout develop

**Create a virtualenv with python 3 binary**

Billjobs was initially written with __python 2.7__ and move to __python 3.x__
It works with __python 3.5__

Read [virtualenv documentation](http://virtualenvwrapper.readthedocs.org/en/latest/ "Virtualenv")

    mkvirtualenv django-billjobs --python=/path/to/python3.5
    add2virtualenv path/to/django-billjobs

**Install dependencies**

    pip install -r requirements_dev.txt

**Sample settings**

The *core/* folder contains sample settings for development. Use DJANGO_SETTINGS_MODULE environment variables.

In your virtualenv *bin/postactivate*

    export DJANGO_SETTINGS_MODULE=core.settings

In your virtualenv *bin/postdeactivate*

    unser DJANGO_SETTINGS_MODULE

You can run server to test your development with :

    django-admin runserver

**Database**

Development use sqlite3 engine.

    django-admin migrate

You can use development fixtures

    django-admin loaddata billjobs/fixtures/dev_data.json

**If you setup a super user it will be deleted by fixtures data.**
- Login : bill
- Password : jobs

