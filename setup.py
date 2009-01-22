from setuptools import setup, find_packages
from flatblocks import get_version

setup(
    name = 'django-flatblocks',
    version = get_version(),
    description = 'django-flatblocks allows you to associate a piece of html '
                  'code with some unique key, and then use this key to insert '
                  'date into a page.',
    long_description = open('README.rst').read(),
    keywords = 'django apps',
    license = 'New BSD License',
    author = 'Horst Gutmann',
    author_email = 'zerok@zerokspot.com',
    url = 'http://github.com/zerok/django-flatblocks/',
    dependency_links = [],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
)

