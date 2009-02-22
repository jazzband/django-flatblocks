from django.db import models
from django.utils.translation import ugettext_lazy as _

class FlatBlock(models.Model):
    """
    Think of a flatblock as a flatpage but for just part of a site. It's
    basically a piece of content with a given name (slug) and an optional
    title (header) which you can, for example, use in a sidebar of a website.
    """
    slug = models.CharField(max_length=255, unique=True, 
                verbose_name=_('Slug'),
                help_text=_(_("A unique name used for reference in the templates")))
    header = models.CharField(blank=True, null=True, max_length=255,
                verbose_name=_('Header'),
                help_text=_(_("An optional header for this content")))
    content = models.TextField(verbose_name=_('Content'), blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.slug,)

