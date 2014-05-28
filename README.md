Billjobs
========

A django billing app for coworking space.

This app is designed to manage bills for the coworking space **Cowork'in Montpellier**.
We intend to stay easy and lite. You can manage coworkers informations and their respective bills.

No tax management.  There is no tax for non-profit organization in France. This application doesn't manage tax, it only 
displays legal French informations and tax 0% on bills.

###User and Group

User and Group management is providing by [django auth](https://docs.djangoproject.com/en/dev/topics/auth/) module.

###Billing

Billing application provide two features **bills** and **services**

Bills module allow you to list, create, modify or delete bills. You can generate a pdf and download it.
You can change **services** default price. Total amount of bill is computed automatically after save. Bill number is 
also set automatically after save.

Service module allow you to list, create, modify or delete services.

Organisation
------------

Billjobs project is using [git flow](http://nvie.com/posts/a-successful-git-branching-model/)

**develop** branch is for development.
**master** branch contains last release.

Installation
------------

**Clone the repository**

    git clone https://github.com/ioO/billjobs.git

**Create a virtualenv with python 2 binary**
Read [virtualenv documentation](http://virtualenvwrapper.readthedocs.org/en/latest/ "Virtualenv")

    mkvirtualenv billjobs --python=/path/to/python2

**Install dependencies**

    pip install -r requirements_dev.txt

File *requirements_prod.txt* removes dependencies like *django debug toolbar* which aren't recommended to deploy in 
production environment.


Licence
=======

This application is under [MIT License](http://en.wikipedia.org/wiki/MIT_License "MIT License") see *LICENSE.md* file.
