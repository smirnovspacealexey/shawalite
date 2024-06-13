from django.contrib import admin
from .models import ExcelBase, PopularNote, NoteBTN
from .backend import excel_to_base
from django.utils.safestring import mark_safe


def parse_to_base(modeladmin, request, queryset):
    excel_base = queryset.first()
    excel_to_base(excel_base.excel.path)


parse_to_base.short_description = 'отпарсить в базу'


def parse_to_base(modeladmin, request, queryset):
    excel_base = queryset.first()
    excel_to_base(excel_base.excel.path)


parse_to_base.short_description = 'отпарсить в базу'


@admin.register(ExcelBase)
class ExcelBaseAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'excel', ]
    list_editable = ('name', 'excel')
    search_fields = ['name', ]
    actions = [parse_to_base, ]


@admin.register(PopularNote)
class PopularNoteAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'note', 'position', ]


@admin.register(NoteBTN)
class NoteBTNAdmin(admin.ModelAdmin):
    list_display = ['preview', 'picture', 'note', 'position', 'active']
    list_editable = ('note', 'position', 'picture', 'active')
    fields = ('preview', 'picture', 'note', 'position', 'active')
    readonly_fields = ["preview"]

    def preview(self, obj):
        try:
            return mark_safe(f'<img src="{obj.picture.url}" style="max-width: 50px;">')
        except:
            return ''

