from django.contrib import admin

from .models import Topic, Entry
#models shows in the admin panel
admin.site.register(Topic)
admin.site.register(Entry)
