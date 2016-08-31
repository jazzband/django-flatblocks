#!/usr/bin/env python

# Adapted from https://raw.githubusercontent.com/hzy/django-polarize/master/runtests.py

import sys

from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.auth',
            'django.contrib.admin',
            'flatblocks',
            'tests',
        ),
        ROOT_URLCONF='tests.urls',
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'debug': True
                }
            },
        ],
    )


def runtests():
    argv = sys.argv[:1] + ['test', 'tests']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
