import os
from django.conf.global_settings import *

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
#sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

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
    'flatblocks',
)
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
        'django.core.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        )
LANGUAGE_CODE = "en"
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)
ROOT_URLCONF = 'test_project.urls'
SECRET_KEY = "12345"
