from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path
from flatblocks.views import edit

urlpatterns = [
    re_path(
        r"^edit/(?P<pk>\d+)/$",
        staff_member_required(edit),
        name="flatblocks-edit",
    ),
]
