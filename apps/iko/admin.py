from django.contrib import admin
from .models import iikoSettings, IkoOrder


@admin.register(iikoSettings)
class iikoSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'url', 'active', 'lat_req', 'lat_token']
    list_editable = ('url', 'active', )


@admin.register(IkoOrder)
class IkoOrderAdmin(admin.ModelAdmin):
    list_display = ['ikoid', 'number', 'datetime', 'is_voiced']
    list_editable = ('is_voiced',)
