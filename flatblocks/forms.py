from django.forms import ModelForm

from flatblocks.models import FlatBlock


class FlatBlockForm(ModelForm):
    class Meta:
        model = FlatBlock
        exclude = ('slug', )
