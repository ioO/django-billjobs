import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-billjobs',
    version='0.2.2',
    packages=['billjobs'],
    include_package_data=True,
    license='X11 License',
    description='A django billing app for coworking space.',
    long_description=README,
    url='https://github.com/ioO/django-billjobs',
    author='Lionel Chanson',
    author_email='github@lionelchanson.fr',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Coworking space',
        'License :: X11 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Framework :: Django :: 1.8.x',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
