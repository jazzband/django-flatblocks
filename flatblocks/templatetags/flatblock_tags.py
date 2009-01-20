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
        
        This field is option and defaults to no caching.
        
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
from django.db import models
from django.core.cache import cache

register = template.Library()

FlatBlock = models.get_model('flatblocks', 'flatblock')
CACHE_PREFIX = "flatblock_"

class BasicFlatBlockWrapper(object):
    def prepare(self, parser, token):
        tokens = token.split_contents()
        self.is_variable = False
        self.slug = None
        if len(tokens) < 2 or len(tokens) > 3:
            raise template.TemplateSyntaxError, "%r tag should have either 2 or 3 arguments" % (tokens[0],)
        if len(tokens) == 2:
            tag_name, slug = tokens
            self.cache_time = 0
        if len(tokens) == 3:
            tag_name, slug, self.cache_time = tokens
        # Check to see if the slug is properly double/single quoted
        if not (slug[0] == slug[-1] and slug[0] in ('"', "'")):
            self.is_variable = True
            self.slug = slug
        else:
            self.slug = slug[1:-1]
    
    def __call__(self, parser, token):
        self.prepare(parser, token)
        return FlatBlockNode(self.slug, self.is_variable, self.cache_time)

class PlainFlatBlockWrapper(BasicFlatBlockWrapper):
    def __call__(self, parser, token):
        self.prepare(parser, token)
        return FlatBlockNode(self.slug, self.is_variable, self.cache_time, False)

do_get_flatblock = BasicFlatBlockWrapper()
do_plain_flatblock = PlainFlatBlockWrapper()
    
class FlatBlockNode(template.Node):
    def __init__(self, slug, is_variable, cache_time=0, with_template=True):
       self.slug = slug
       self.is_variable = is_variable
       self.cache_time = cache_time
       self.with_template = with_template
    
    def render(self, context):
        if self.is_variable:
            real_slug = template.Variable(self.slug).resolve(context)
        else:
            real_slug = self.slug
        # Eventually we want to pass the whole context to the template so that
        # users have the maximum of flexibility of what to do in there.
        if self.with_template:
            new_ctx = template.Context({})
            new_ctx.update(context)
        try:
            cache_key = CACHE_PREFIX + real_slug
            c = cache.get(cache_key)
            if c is None:
                c = FlatBlock.objects.get(slug=real_slug)
                cache.set(cache_key, c, int(self.cache_time))
            if self.with_template:
                tmpl = template.loader.get_template('flatblocks/flatblock.html')
                new_ctx.update({'flatblock':c})
                return tmpl.render(new_ctx)
            else:
                return c.content
        except FlatBlock.DoesNotExist:
            return ''

register.tag('flatblock', do_get_flatblock)
register.tag('plain_flatblock', do_plain_flatblock)