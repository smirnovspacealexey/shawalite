from django.contrib import admin
from models import likoSettings


@admin.register(likoSettings)
class likoSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'url', 'active']
    list_editable = ('url', 'active', )




