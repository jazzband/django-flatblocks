from django.db import models

class FreeText(models.Model):
    """
    A FreeText is a piece of content associated
    with a unique key that can be inserted into
    any template with the use of a special template
    tag
    """
    key = models.CharField('key', help_text="A unique name for this FreeText of content", blank=False, maxlength=255, unique=True)
    content = models.TextField('content', blank=True)
    active = models.BooleanField("active", default=False)

    class Meta:
        verbose_name = 'free text'
        verbose_name_plural = 'free texts'

    def __unicode__(self):
        return u"%s" % (self.key,)

