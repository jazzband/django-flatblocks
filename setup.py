from setuptools import setup, find_packages


setup(
    name='django-flatblocks',
    version='0.9.1',
    description='django-flatblocks acts like django.contrib.flatpages but '
                'for parts of a page; like an editable help box you want '
                'show alongside the main content.',
    long_description=open('README.rst').read(),
    keywords='django apps',
    license='New BSD License',
    author='Horst Gutmann, Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/django-flatblocks/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=find_packages(exclude=['test_project']),
    package_data={
        'flatblocks': [
            'templates/flatblocks/*.html',
            'locale/*/*/*.mo',
            'locale/*/*/*.po',
        ]
    },
    zip_safe=False,
    requires = [
        'Django (>=1.4)',
    ],
)
