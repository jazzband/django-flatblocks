from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.shortcuts import render

urlpatterns = [
    url('^flatblocks/', include("flatblocks.urls")),
    url('^admin/', admin.site.urls),
    url('^$', render, {'template_name': 'index.html'}),
]
