import os
import errno

from os.path import join, abspath, dirname


# Snippet from Two Scoops of Django 1.6 to get relative directories
here = lambda *dirs: join(abspath(dirname(__file__)), *dirs)
BASE_DIR = here("..", "..")
root = lambda *dirs: join(abspath(BASE_DIR), *dirs)


# From: https://stackoverflow.com/a/273227
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
