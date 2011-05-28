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
from django.db import models
from django.core.cache import cache

from flatblocks import settings

import logging


register = template.Library()
logger = logging.getLogger(__name__)

FlatBlock = models.get_model('flatblocks', 'flatblock')

class BasicFlatBlockWrapper(object):
    def prepare(self, parser, token):
        """
        The parser checks for following tag-configurations::

            {% flatblock {block} %}
            {% flatblock {block} {timeout} %}
            {% flatblock {block} using {tpl_name} %}
            {% flatblock {block} {timeout} using {tpl_name} %}
        """
        tokens = token.split_contents()
        self.is_variable = False
        self.tpl_is_variable = False
        self.slug = None
        self.cache_time = 0
        self.tpl_name = None
        tag_name, self.slug, args = tokens[0], tokens[1], tokens[2:]
        num_args = len(args)
        if num_args == 0:
            # Only the block name was specified
            pass
        elif num_args == 1:
            # block and timeout
            self.cache_time = args[0]
            pass
        elif num_args == 2:
            # block, "using", tpl_name
            self.tpl_name = args[1]
        elif num_args == 3:
            # block, timeout, "using", tpl_name
            self.cache_time = args[0]
            self.tpl_name = args[2]
        else:
            raise template.TemplateSyntaxError, "%r tag should have between 1 and 4 arguments" % (tokens[0],)
        # Check to see if the slug is properly double/single quoted
        if not (self.slug[0] == self.slug[-1] and self.slug[0] in ('"', "'")):
            self.is_variable = True
        else:
            self.slug = self.slug[1:-1]
        # Clean up the template name
        if self.tpl_name is not None:
            if not(self.tpl_name[0] == self.tpl_name[-1] and self.tpl_name[0] in ('"', "'")):
                self.tpl_is_variable = True
            else:
                self.tpl_name = self.tpl_name[1:-1]
        if self.cache_time is not None and self.cache_time != 'None':
            self.cache_time = int(self.cache_time)

    def __call__(self, parser, token):
        self.prepare(parser, token)
        return FlatBlockNode(self.slug, self.is_variable, self.cache_time,
                template_name=self.tpl_name,
                tpl_is_variable=self.tpl_is_variable)

class PlainFlatBlockWrapper(BasicFlatBlockWrapper):
    def __call__(self, parser, token):
        self.prepare(parser, token)
        return FlatBlockNode(self.slug, self.is_variable, self.cache_time, False)

do_get_flatblock = BasicFlatBlockWrapper()
do_plain_flatblock = PlainFlatBlockWrapper()

class FlatBlockNode(template.Node):
    def __init__(self, slug, is_variable, cache_time=0, with_template=True,
            template_name=None, tpl_is_variable=False):
        if template_name is None:
            self.template_name = 'flatblocks/flatblock.html'
        else:
            if tpl_is_variable:
                self.template_name = template.Variable(template_name)
            else:
                self.template_name = template_name
        self.slug = slug
        self.is_variable = is_variable
        self.cache_time = cache_time
        self.with_template = with_template

    def render(self, context):
        if self.is_variable:
            real_slug = template.Variable(self.slug).resolve(context)
        else:
            real_slug = self.slug
        if isinstance(self.template_name, template.Variable):
            real_template = self.template_name.resolve(context)
        else:
            real_template = self.template_name
        # Eventually we want to pass the whole context to the template so that
        # users have the maximum of flexibility of what to do in there.
        if self.with_template:
            new_ctx = template.Context({})
            new_ctx.update(context)
        try:
            flatblock = None
            if self.cache_time != 0:
                cache_key = settings.CACHE_PREFIX + real_slug
                flatblock = cache.get(cache_key)
            if flatblock is None:

                # if flatblock's slug is hard-coded in template then it is
                # safe and convenient to auto-create block if it doesn't exist.
                # This behaviour can be configured using the
                # FLATBLOCKS_AUTOCREATE_STATIC_BLOCKS setting
                if self.is_variable or not settings.AUTOCREATE_STATIC_BLOCKS:
                    flatblock = FlatBlock.objects.get(slug=real_slug)
                else:
                    flatblock, _ = FlatBlock.objects.get_or_create(
                                      slug=real_slug,
                                      defaults = {'content': real_slug}
                                   )
                if self.cache_time != 0:
                    if self.cache_time is None or self.cache_time == 'None':
                        logger.debug("Caching %s for the cache's default timeout"
                                % (real_slug,))
                        cache.set(cache_key, flatblock)
                    else:
                        logger.debug("Caching %s for %s seconds" % (real_slug,
                            str(self.cache_time)))
                        cache.set(cache_key, flatblock, int(self.cache_time))
                else:
                    logger.debug("Don't cache %s" % (real_slug,))

            if self.with_template:
                tmpl = loader.get_template(real_template)
                new_ctx.update({'flatblock':flatblock})
                return tmpl.render(new_ctx)
            else:
                return flatblock.content
        except FlatBlock.DoesNotExist:
            return ''

register.tag('flatblock', do_get_flatblock)
register.tag('plain_flatblock', do_plain_flatblock)
