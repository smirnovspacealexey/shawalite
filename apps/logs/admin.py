from django.contrib import admin
from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'title2', 'title3', 'logg', 'datetime']
    list_editable = ('name',)
    search_fields = ['name', 'title2', 'title3']
    list_filter = ['datetime', ]




