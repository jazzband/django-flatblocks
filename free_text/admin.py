from django.contrib import admin
from free_text.models import FreeText
 
class FreeTextAdmin(admin.ModelAdmin):
    ordering = ['slug',]
    list_display = ('slug', 'header', 'content')
    search_fields = ('slug', 'header', 'content')

admin.site.register(FreeText, FreeTextAdmin)