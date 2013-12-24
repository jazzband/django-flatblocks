
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class FlatBlock(models.Model):
    """
    Think of a flatblock as a flatpage but for just part of a site. It's
    basically a piece of content with a given name (slug) and an optional
    title (header) which you can, for example, use in a sidebar of a website.
    """
    slug = models.CharField(_('Slug'), max_length=255, unique=True,
        help_text=_("A unique name used for reference in the templates")
    )
    header = models.CharField(_('Header'), blank=True, max_length=255,
        help_text=_("An optional header for this content")
    )
    content = models.TextField(verbose_name=_('Content'), blank=True)

    # Helper attributes used if content should be evaluated in order to
    # represent the original content.
    raw_content = None
    raw_header = None

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = _('Flat block')
        verbose_name_plural = _('Flat blocks')
