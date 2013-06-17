from distutils.core import setup

setup(
    name='django-flatblocks',
    version='0.7.1',
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
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
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
    }
)
