import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

DEBUG=True
TEMPLATE_DEBUG=True
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/flatblocks.db'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'flatblocks',
)
LANGUAGE_CODE="no"
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)
ROOT_URLCONF = 'urls'
