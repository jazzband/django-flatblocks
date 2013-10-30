try:
    from setuptools import setup
    kws = {'install_requires': ['Django']}
except:
    from distutils.core import setup
    kws = {}


setup(
    name='django-flatblocks',
    version='0.8',
    description='django-flatblocks acts like django.contrib.flatpages but '
                'for parts of a page; like an editable help box you want '
                'show alongside the main content.',
    long_description=open('README.rst').read(),
    keywords='django apps',
    license='New BSD License',
    author='Horst Gutmann',
    author_email='zerok@zerokspot.com',
    url='http://github.com/zerok/django-flatblocks/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=['flatblocks', 'flatblocks.management',
              'flatblocks.management.commands', 'flatblocks.migrations',
              'flatblocks.templatetags'],
    package_data={
        'flatblocks': [
            'templates/flatblocks/*.html',
            'locale/*/*/*.mo',
            'locale/*/*/*.po',
        ]
    },
    **kws
)
