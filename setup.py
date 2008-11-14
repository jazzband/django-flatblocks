from setuptools import setup, find_packages

setup(
    name = 'django-freetext',
    version = '0.1.0',
    description = 'django-freetext allows you to associate a piece of html code '
                  'with some unique key, and then use this key to insert date into a page.',
    long_description = open('README.md').read(),
    keywords = 'django apps',
    license = 'New BSD License',
    author = 'Kevin Fricovsky',
    author_email = 'kevin@howiworkdaily.com',
    maintainer = 'Alexander Artemenko',
    maintainer_email = 'svetlyak.40wt@gmail.com',
    url = 'http://github.com/svetlyak40wt/django-freetext/',
    dependency_links = [],
    classifiers=[
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
)

