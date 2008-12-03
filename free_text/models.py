from django.db import models

class FreeText(models.Model):
    """
    A FreeText is a piece of content associated with a unique key that 
    can be inserted into any template with the use of a special template
    tag
    """
    slug = models.CharField(max_length=255, unique=True
                help_text="A unique name for this content")
    content = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.key,)

