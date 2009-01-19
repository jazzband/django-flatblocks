django-freetext
================

django-freetext is a simple application for handling small text-blocks on
websites. Think about it like ``django.contrib.flatpages`` just not for a 
whole page but for only parts of it, like an information text describing what
you can do on a site.

Usage
------------

Once you've created some instances of the ``free_text.models.FreeText`` model, 
you can load it it using the ``freetext`` templatetag-library::
    
    {% load freetext %}
    
    <html>
        <head>
            <!-- ... -->
        </head>
        <body>
            <div id="page">
                <div id="main">
                    <!-- ... -->
                </div>
                <div id="sidebar">
                    {% freetext "page.info" %}
                </div>
            </div>
        </body>
    </html>

This way you can display a text block with the name 'page.info'. If you 
have the name of a block in a template variable, leave out the quotes.

This tag also accepts an optional argument where you can specify the number
of seconds, the that block should be cached::
    
    {% freetext "page.info" 3600 %}


History
------------

Since this application targets use-cases that are basically applicable to 
most web-projects out there, there are tons of solutions similar to this one.
In fact, this app is a fork originally from `django-chunks`_ developed by 
Clint Ecker.

In November 2008 Kevin Fricovsky created the `original fork`_ in order to add
an additional "active"-flag to each chunk. That project was later on `forked 
by Peter Baumgardner`_ who removed that flag again and added a "header"-field 
in order to directly associate and optional title with each text block.

This fork aims now to add more features like variable chunks and also
integrate some of the features developed by Håkan Waara and Sam Cranford in
the `django-better-chunks`_ fork (``django.contrib.site``- and i18n-support).


.. _`original fork`: http://github.com/howiworkdaily/django-freetext/
.. _`django-chunks`: http://code.google.com/p/django-chunks/
.. _`django-better-chunks`: http://bitbucket.org/hakanw/django-better-chunks/
.. _`forked by Peter Baumgardner`: http://github.com/lincolnloop/django-freetext/