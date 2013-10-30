try:
    from django.conf.urls import patterns, url, include
except ImportError:  # Django < 1.4
    from django.conf.urls.defaults import patterns, url, include
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = patterns('',
    url('^flatblocks/', include("flatblocks.urls")),
    url('^admin/', include(admin.site.urls)),
    url('^/?', views.index),
)
