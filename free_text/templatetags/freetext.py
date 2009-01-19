"""
This module offers one templatetag called "freetext" which allows you to
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
    
    {% load freetext %}
    
    ...
    
    {% freetext 'contact_help' %}
    {% freetext name_in_variable %}
    

"""

from django import template
from django.db import models
from django.core.cache import cache

register = template.Library()

FreeText = models.get_model('free_text', 'freetext')
CACHE_PREFIX = "freetext_"

def do_get_freetext(parser, token):
    # split_contents() knows not to split quoted strings.
    tokens = token.split_contents()
    is_variable = False
    real_slug = None
    if len(tokens) < 2 or len(tokens) > 3:
        raise template.TemplateSyntaxError, "%r tag should have either 2 or 3 arguments" % (tokens[0],)
    if len(tokens) == 2:
        tag_name, slug = tokens
        cache_time = 0
    if len(tokens) == 3:
        tag_name, slug, cache_time = tokens
    # Check to see if the slug is properly double/single quoted
    if not (slug[0] == slug[-1] and slug[0] in ('"', "'")):
        is_variable = True
        real_slug = slug
    else:
        real_slug = slug[1:-1]
    # Send slug without quotes and caching time
    return FreeTextNode(real_slug, is_variable, cache_time)
    
class FreeTextNode(template.Node):
    def __init__(self, slug, is_variable, cache_time=0):
       self.slug = slug
       self.is_variable = is_variable
       self.cache_time = cache_time
    
    def render(self, context):
        if self.is_variable:
            real_slug = template.Variable(self.slug).resolve(context)
        else:
            real_slug = self.slug
        try:
            cache_key = CACHE_PREFIX + real_slug
            c = cache.get(cache_key)
            if c is None:
                c = FreeText.objects.get(slug=real_slug)
                cache.set(cache_key, c, int(self.cache_time))
            tmpl = template.loader.get_template('freetext/freetext.html')
            if 'request' in context:
                ctx = template.RequestContext(context['request'], {'freetext': c})
            else:
                ctx = template.Context({'freetext': c})
            return tmpl.render(ctx)
        except FreeText.DoesNotExist:
            return ''
        
register.tag('freetext', do_get_freetext)
