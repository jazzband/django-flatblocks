1.0.0:
    * Add support for Django 2.2, 3.0, and 3.1.
    * Add support for Python 3.6, 3.7, 3.8 and 3.9.
    * Remove support for Django 1.7, 1.8, 1.9, 1.10, and 1.11.
    * Remove support for Python 3.4 and 3.5.
    * Move CI to GitHub Actions: https://github.com/jazzband/django-flatblocks/actions

0.9.4:
    * Drop Python 3.3 support.
    * Add support for Django 1.11.

0.9.3:
    * Fixed Django 1.10 compatibility

0.9.2:
    * Fixed reading of README in setup.py
    * Dropped Django 1.4 testing
    * Tidied code with flake8 and isort
    * Fix support for Django 1.7+
    * Fix packaging to exclude tests module

0.9.1:
    * Dropped testing of Django 1.5 and 1.6
    * Added migrations [Thanks Sergey Fedoseev]

0.9:
    NOTE: Major tag syntax changes!

    * Modernised to use simple_tag and standard kwarg syntax.
    * Removed caching - use {% cache %} tag instead

0.8:
    * Python 3 & Django 1.6 support

0.7:
    * Support for evaluated blocks offering access to context variables

0.6:
    * South support
    * Installation and upgrade instructions

    Note: This is primarily a transitional release to get South in here and
    open this project up for some database changes in the future.

0.5.1
    * Removed rendering of the content attribute from the admin list by Michael Fladischer
    * PyBabel compatibility by Michael Fladischer
    * Fixed caching issue with memcache backend

0.5
    * Hungarian translation by Török Gábor
    * Method added to demo edit form (#5) by Bill Evans

0.4
    * FlatBlock autocreation by Mikhail Korobov (can be enabled/disabled
      with FLATBLOCKS\_AUTOCREATE\_STATIC\_BLOCKS setting)
    * Various fixes by Mikhail Korobov
    * Fix by Henrik Heimbuerger for the manifest

0.3.5
    * Russian translation by Mikhail Korobov

0.3.4
    * Norwegian translation by Eivind Uggedal

0.3.3
    * FlatBlock.save should also accept optional kwargs.

0.3.2
    * All settings are now in the flatblocks.settings module

0.3.1
    * Fixes a bug with FlatBlock.save() failing to reset the cache
    * Buildout integration for easier testing
    * Example urls.py and flatblocks/edit.html-template

0.3
    * createflatblock and deleteflatblock commands
    * On saving a flatblock its cache will be cleared
    * As last argument of the template tag you can now also specify a template
      name.
0.2
    * Translatable
    * ``flatblocks.views.edit`` view for editing flatblocks
0.1
    Initial release
