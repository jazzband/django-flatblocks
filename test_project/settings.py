import os
import sys
from django.conf.global_settings import *

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

SITE_ID = 1
DEBUG = True
TEMPLATE_DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'test.db')
    }
}
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'flatblocks',
)

try:
    import south
    INSTALLED_APPS += ('south',)
except ImportError, _:
    pass

LANGUAGE_CODE = "en"

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)
ROOT_URLCONF = 'test_project.urls'
SECRET_KEY = "12345"
