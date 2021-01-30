from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

urlpatterns = [
    path('flatblocks/', include("flatblocks.urls")),
    path('admin/', admin.site.urls),
    path('', render, {'template_name': 'index.html'}),
]
