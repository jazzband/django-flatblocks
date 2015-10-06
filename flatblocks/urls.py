from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from flatblocks.views import edit

urlpatterns = [
    url('^edit/(?P<pk>\d+)/$',
        staff_member_required(edit),
        name='flatblocks-edit'),
]
