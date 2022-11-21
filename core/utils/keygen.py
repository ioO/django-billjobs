"""
Two things are wrong with Django's default `SECRET_KEY` system:

1. It is not random but pseudo-random
2. It saves and displays the SECRET_KEY in `settings.py`

This snippet
1. uses `SystemRandom()` instead to generate a random key
2. saves a local `secret.txt`

The result is a random and safely hidden `SECRET_KEY`.

From https://gist.github.com/ndarville/3452907
Edited by Thomas Maurin, 2014 to run on python3
"""
try:
    SECRET_KEY
except NameError:
    from os.path import join
    from .path import BASE_DIR, make_sure_path_exists
    make_sure_path_exists(join(BASE_DIR, 'secrets'))
    SECRET_FILE = join(BASE_DIR, 'secrets', 'secret.txt')
    try:
        with open(SECRET_FILE) as f:
            SECRET_KEY = f.read().strip()
    except IOError:
        try:
            import random
            SECRET_KEY = ''.join([random.SystemRandom().choice(
                'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                for i in range(50)])
            secret = open(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a {:s} file with random characters \
            to generate your secret key!'.format(SECRET_FILE))
