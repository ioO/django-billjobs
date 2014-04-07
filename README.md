Billjobs
========

A django billing app for coworking space

This app is designed to manage bills for the coworking space **Cowork'in Montpellier**.
We intend to stay easy and lite. You can manage coworkers information and their respective bills.
We do not use permission system, because each coworker can make is own bills every months, and can also add a new 
coworker. But we use django and it's own user management application. User and group permissions are available.

Installation
------------

**Clone the repository**

    git clone https://github.com/ioO/billjobs.git

**Create a virtualenv with python 2 binary**
Read [virtualenv documentation](http://virtualenvwrapper.readthedocs.org/en/latest/ "Virtualenv")

    mkvirtualenv billjobs --python=/path/to/python2

**Install dependencies**

    pip install -r requirements_dev.txt

File *requirements_prod.txt* remove dependencies like *django debug toolbar* which aren't recommended to deploy in 
production environment.


Licence
=======

MIT
