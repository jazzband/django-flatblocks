import os
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
    os.path.join(os.path.dirname(__file__), 'templates'),
)
ROOT_URLCONF = 'test_project.urls'
