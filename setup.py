import io

from setuptools import setup, find_packages


setup(
    name='django-flatblocks',
    version='1.0.0',
    description='django-flatblocks acts like django.contrib.flatpages but '
                'for parts of a page; like an editable help box you want '
                'show alongside the main content.',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    keywords='django apps',
    license='New BSD License',
    author='Horst Gutmann, Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='http://github.com/funkybob/django-flatblocks/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=find_packages(exclude=['tests']),
    package_data={
        'flatblocks': [
            'templates/flatblocks/*.html',
            'locale/*/*/*.mo',
            'locale/*/*/*.po',
        ]
    },
    zip_safe=False,
    requires = [
        'Django (>=2.2)',
    ],
)
