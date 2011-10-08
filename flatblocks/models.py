from django.db import models
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from flatblocks.settings import CACHE_PREFIX


class FlatBlock(models.Model):
    """
    Think of a flatblock as a flatpage but for just part of a site. It's
    basically a piece of content with a given name (slug) and an optional
    title (header) which you can, for example, use in a sidebar of a website.
    """
    slug = models.CharField(max_length=255,
                verbose_name=_('Slug'),
                help_text=_("A unique name used for reference in the templates"))
    header = models.CharField(blank=True, null=True, max_length=255,
                verbose_name=_('Header'),
                help_text=_("An optional header for this content"))
    content = models.TextField(verbose_name=_('Content'), blank=True, null=True)
    sites = models.ManyToManyField(Site)

    objects = models.Manager()
    site_objects = CurrentSiteManager()

    def __unicode__(self):
        return u"%s" % (self.slug,)
    
    def save(self, *args, **kwargs):
        super(FlatBlock, self).save(*args, **kwargs)
        # Now also invalidate the cache used in the templatetag
        cache.delete('%s%s' % (CACHE_PREFIX, self.slug, ))

    def validate_unique(self, exclude=None):
        """
        Validates the uniqueness of the slug with respect to the associated sites.
        """
        super(FlatBlock, self).validate_unique(exclude)
        if not self.pk or (exclude and 'sites' in exclude):
            return
        validate_site_uniqueness(self)

    class Meta:
        verbose_name = _('Flat block')
        verbose_name_plural = _('Flat blocks')

def validate_site_uniqueness(block, site_pks=None):
    """
    Enforces that slug and site are unique.
    """
    if site_pks is None:
        site_pks = [site.pk for site in block.sites.all()]
    for site_pk in site_pks:
        for other in FlatBlock.objects.filter(slug=block.slug).filter(sites=site_pk):
            if other != block:
                raise ValidationError, "slug is not unique for the selected sites"

@receiver(models.signals.m2m_changed, sender=FlatBlock.sites.through)
def check_m2m_add(sender, **kwargs):
    instance = kwargs.get('instance')
    action = kwargs.get('action')
    pk_set = kwargs.get('pk_set')
    reverse = kwargs.get('reverse', False)
    site_pks = pk_set
    block = instance # If done normally
    if reverse:
        block = kwargs.get('model').objects.get(pk=pk_set.__iter__().next())
        site_pks = [instance.pk]
    if action == 'pre_add':
        try:
            validate_site_uniqueness(block, site_pks)
        except ValidationError, e:
            raise IntegrityError, e
