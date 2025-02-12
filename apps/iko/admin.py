from django.contrib import admin
from .models import iikoSettings, IkoOrder, AudioNumber


@admin.register(iikoSettings)
class iikoSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'url', 'active', 'lat_req', 'lat_token']
    list_editable = ('url', 'active', )


@admin.register(IkoOrder)
class IkoOrderAdmin(admin.ModelAdmin):
    list_display = ['ikoid', 'number', 'datetime', 'is_voiced']
    list_editable = ('is_voiced',)


@admin.register(AudioNumber)
class AudioNumberAdmin(admin.ModelAdmin):
    list_display = ['name', 'audio',]
