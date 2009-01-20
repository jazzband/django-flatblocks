from django.db import models
from django.utils.translation import ugettext_lazy as _

class FlatBlock(models.Model):
    """
    A piece of content associated with a unique slug that can be inserted 
    into any template with the use of a special template tag.
    
    """
    slug = models.CharField(max_length=255, unique=True,
                help_text=_("A unique name used for reference in the templates"))
    header = models.CharField(blank=True, null=True, max_length=255,
                help_text=_("An optional header for this content"))
    content = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.slug,)

