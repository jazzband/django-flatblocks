"""
This module offers one templatetag called "freetext" which allows you to
easily embed small text-snippets (like for example the help section of a page)
into a template.

It accepts 2 parameter:

    slug
        The slug/key of the text (for example 'contact_help'). This slug has
        to be passed with quotes to the templatetag.

    cache_time
        The number of seconds that text should get cached after it has been
        fetched from the database.
        
        This field is option and defaults to no caching.
        
Example::
    
    {% load freetext %}
    
    ...
    
    {% freetext 'contact_help' %}
    

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
    if len(tokens) < 2 or len(tokens) > 3:
        raise template.TemplateSyntaxError, "%r tag should have either 2 or 3 arguments" % (tokens[0],)
    if len(tokens) == 2:
        tag_name, slug = tokens
        cache_time = 0
    if len(tokens) == 3:
        tag_name, slug, cache_time = tokens
    # Check to see if the slug is properly double/single quoted
    if not (slug[0] == slug[-1] and slug[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    # Send slug without quotes and caching time
    return FreeTextNode(slug[1:-1], cache_time)
    
class FreeTextNode(template.Node):
    def __init__(self, slug, cache_time=0):
       self.slug = slug
       self.cache_time = cache_time
    
    def render(self, context):
        try:
            cache_key = CACHE_PREFIX + self.slug
            c = cache.get(cache_key)
            if c is None:
                c = FreeText.objects.get(slug=self.slug)
                cache.set(cache_key, c, int(self.cache_time))
            content = c.content
        except FreeText.DoesNotExist:
            content = ''
        return content
        
register.tag('freetext', do_get_freetext)
