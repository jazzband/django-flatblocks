"""
This module offers one templatetag called "flatblock" which allows you to
easily embed small text-snippets (like for example the help section of a page)
into a template.

It accepts 2 parameter:

    slug
        The slug/key of the text (for example 'contact_help'). There are two
        ways you can pass the slug to the templatetag: (1) by its name or
        (2) as a variable.

        If you want to pass it by name, you have to use quotes on it.
        Otherwise just use the variable name.

    cache_time
        The number of seconds that text should get cached after it has been
        fetched from the database.

        This field is optional and defaults to no caching (0).

        To use Django's default caching length use None.

Example::

    {% load flatblock_tags %}

    ...

    {% flatblock 'contact_help' %}
    {% flatblock name_in_variable %}

The 'flatblock' template tag acts like an inclusiontag and operates on the
``flatblock/flatblock.html`` template file, which gets (besides the global
context) also the ``flatblock`` variable passed.

Compared to the original implementation this includes not only the block's
content but the whole object inclusing title, slug and id. This way you
can easily for example offer administrative operations (like editing)
within that template.

"""

from django import template
from django.template import loader
from django.template.loader import render_to_string
from django.db import models
from django.core.cache import cache

from flatblocks import settings

import logging


register = template.Library()
logger = logging.getLogger(__name__)

FlatBlock = models.get_model('flatblocks', 'flatblock')


@register.simple_tag(takes_context=True)
def flatblock(context, slug, timeout=None, evaluated=False, using='flatblocks/flatblock.html'):

    if timeout:
        # Build Key from slug/evaluated/using
        cache_key = ':'.join(map(str, [slug, evaluated, using]))
        result = cache.get(cache_key)
        if result is not None:
            return result

    if not settings.AUTOCREATE_STATIC_BLOCKS:
        try:
            flatblock = FlatBlock.objects.get(slug=slug)
        except FlatBlock.DoesNotExist:
            return ''
    else:
        flatblock, _ = FlatBlock.objects.get_or_create(
            slug=slug,
            defaults={'content': slug}
        )

    if evaluated:
        flatblock.raw_content = flatblock.content
        flatblock.raw_header = flatblock.header
        flatblock.content = template.Template(flatblock.content).render(context)
        flatblock.header = template.Template(flatblock.header).render(context)

    if using:
        context.update({'flatblock': flatblock})
        result = render_to_string(using, context)
        context.pop()
    else:
        result = flatblock.content

    if timeout:
        cache.set(cache_key, result, timeout=float(timeout))

    return result

@register.simple_tag(takes_context=True)
def plain_flatblock(context, slug, timeout=None, evaluated=False):
    return flatblock(context, slug, timeout=timeout, evaluated=evaluated, using=None)

