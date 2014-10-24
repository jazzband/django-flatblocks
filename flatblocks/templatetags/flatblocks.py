"""
This module offers one templatetag called "flatblock" which allows you to
easily embed small text-snippets (like for example the help section of a page)
into a template.

It requires one argument, and accepts several extra keywords:

    {% flatblock {slug} [evaluated={bool}] [using={template}] %}

    slug::
        The slug/key of the text (for example 'contact_help').

    evaluated::
        If set to True, the content and header of the FlatBlock will be
        rendered as a Template before being passed to the template.

        This allows you to embed template tags into your FlatBlocks.

        The original values for the content and header will be saved to
        raw_content and raw_header respectively.

    using::
        The template to render the FlatBlock with.  If not supplied, will
        default to "flatblocks/flatblock.html".

        If set to False, will not be used, and the output of the tag will be
        the ``content`` property of the FlatBlock.

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
from __future__ import absolute_import

from django import template
from django.template.loader import render_to_string
from django.db import models

from flatblocks import settings

import logging


register = template.Library()
logger = logging.getLogger(__name__)

FlatBlock = models.get_model('flatblocks', 'flatblock')


@register.simple_tag(takes_context=True)
def flatblock(context, slug, evaluated=False, using='flatblocks/flatblock.html'):

    if not settings.AUTOCREATE_STATIC_BLOCKS:
        try:
            flatblock = FlatBlock.objects.get(slug=slug)
        except FlatBlock.DoesNotExist:
            return ''
    else:
        flatblock, _ = FlatBlock.objects.get_or_create(slug=slug,
            defaults={'content': slug}
        )

    if evaluated:
        flatblock.raw_content = flatblock.content
        flatblock.raw_header = flatblock.header
        flatblock.content = template.Template(flatblock.content).render(context)
        flatblock.header = template.Template(flatblock.header).render(context)

    if using:
        result = render_to_string(using, {'flatblock': flatblock}, context)
    else:
        result = flatblock.content

    return result


@register.simple_tag(takes_context=True)
def plain_flatblock(context, slug, evaluated=False):
    return flatblock(context, slug, evaluated=evaluated, using=None)
