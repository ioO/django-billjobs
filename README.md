Billjobs
========

A django billing app for coworking space.

This app is designed to manage bills for the coworking space **Cowork'in Montpellier**.
We intend to stay easy and lite. You can manage coworkers informations and their respective bills.
We do not use permission system, because each coworker can make his own bills every month, and can also add a new 
coworker. But we use Django and its own user management application. Users and groups permissions are available.

No tax management.  There is no tax for non-profit organization in France. This application doesn't manage tax, it only 
displays legal French informations and tax 0% on bills.

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
