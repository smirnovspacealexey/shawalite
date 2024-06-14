from django.contrib import admin
from .models import iikoSettings


@admin.register(iikoSettings)
class iikoSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'url', 'active']
    list_editable = ('url', 'active', )



