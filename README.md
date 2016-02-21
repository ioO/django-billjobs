Billjobs
========

A django billing app for coworking space.

We intend to keep things as simple as we can and with an easy user experience. This apps is designed to manage 
coworkers and their bills.

**No tax management**. There is no tax for non-profit organization in France. This application doesn't manage tax, it 
    only displays legal French informations and tax 0% on bills.

We use it at [Cowork'in Montpellier](http://www.coworkinmontpellier.org) and [Le village](http://www.levillage.co/), 
two coworking spaces in South of France.

Features
--------

All the features are managed throught [django admin.site](https://docs.djangoproject.com/en/1.8/ref/contrib/admin/)

- User and Group management is provided by [django auth](https://docs.djangoproject.com/en/dev/topics/auth/) module.
- Billing management
- Services management

Contributing
------------

Wow you are awesome ! Thank you.

### Clone repository

```shell
git clone https://github.com/ioO/billjobs.git
```

### Create a virtualenv with python 3 binary

Billjobs was initially written with **python 2.7** and move to **python 3.x**. It works with **python 3.5**

Read [virtualenv documentation](http://virtualenvwrapper.readthedocs.org/en/latest/ "Virtualenv")

```shell
mkvirtualenv django-billjobs --python=/path/to/python3.5
add2virtualenv path/to/django-billjobs
```

### Install development dependencies

```shell
pip install -r requirements_dev.txt
```

### Sample settings

The *core/* folder contains sample settings for development. Use **DJANGO_SETTINGS_MODULE** environment variables.

In your virtualenv *bin/postactivate*
```shell
export DJANGO_SETTINGS_MODULE=core.settings
```

In your virtualenv *bin/postdeactivate*
```shell
unset DJANGO_SETTINGS_MODULE
```

### Database

Development use sqlite3 engine.
```shell
django-admin migrate
```

### Git workflow

Previously we used [git flow](http://nvie.com/posts/a-successful-git-branching-model/)
**develop** branch is here for historical reason

For now we are using a more simple workflow.

Create a feature branch when you develop a new feature, a hotfix and at the end rebase it with **master** branch.

```shell
git checkout -b new_feature
# do your commits
git checkout master
git pull
git checkout new_feature
git rebase master
git checkout master
git merge --no-ff new_feature
```

### Fixtures

You can use development fixtures
```shell
django-admin loaddata billjobs/fixtures/dev_data.json
```

If you setup a super user it will be deleted by fixtures data.
- Login : bill
- Password : jobs
