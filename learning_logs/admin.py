from django.contrib import admin

from .models import Topic, Entry
#instances available in the admin panel
admin.site.register(Topic)
admin.site.register(Entry)
