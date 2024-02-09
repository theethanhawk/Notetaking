from django.contrib import admin

from .models import Entry, Tag, Link, Image
# Register your models here.

admin.site.register(Entry)
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(Image)