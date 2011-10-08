from django.conf.urls.defaults import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = patterns('',
    url('^flatblocks/', include("flatblocks.urls")),
    url('^admin/', include(admin.site.urls)),
    url('^/?', views.index),
)
