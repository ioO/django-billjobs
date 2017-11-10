import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-billjobs',
    version='0.6.6',
    packages=['billjobs'],
    include_package_data=True,
    install_requires=[
        "django > 1.10",
        "reportlab == 3.4.0",
    ],
    license='X11 License',
    description='A django billing app for coworking space.',
    long_description=README,
    url='https://github.com/ioO/django-billjobs',
    author='Lionel Chanson',
    author_email='github@lionelchanson.fr',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
