from django.contrib import admin
from .models import iikoSettings, IkoOrder, AudioNumber
from django_admin_row_actions import AdminRowActionsMixin

from django.http import HttpResponseForbidden
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect


@admin.register(iikoSettings)
class iikoSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'url', 'active', 'lat_req', 'lat_token']
    list_editable = ('url', 'active', )


@admin.register(IkoOrder)
class IkoOrderAdmin(admin.ModelAdmin):
    list_display = ['ikoid', 'number', 'datetime', 'is_voiced']
    list_editable = ('is_voiced',)


@admin.register(AudioNumber)
class AudioNumberAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'audio')
    list_editable = ('audio',)

    def get_row_actions(self, obj):
        return [
            {
                'label': 'Upload Audio',
                'url': self.get_upload_url(obj.id),
                'method': 'post',
                'enctype': 'multipart/form-data',
            }
        ]

    def get_upload_url(self, obj_id):
        return f'upload/{obj_id}/'

    # def get_form(self, request, obj=None, **kwargs):
    #     Form = super().get_form(request, obj=None, **kwargs)
    #     return functools.partial(Form, user=request.user)
    #
    # def upload_form(self, obj):
    #     """Кастомное поле для отображения формы загрузки аудио."""
    #     return format_html(
    #         '<form id="upload-form-{}" action="{}" method="post" enctype="multipart/form-data">'
    #         '<input type="file" name="audio_file">'
    #         '<button type="button" onclick="uploadAudio({})">Upload</button>'
    #         '</form>',
    #         obj.id,
    #         self.get_upload_url(obj.id),
    #         obj.id
    #     )
    # upload_form.short_description = 'Upload Audio'
    #
    # def get_upload_url(self, obj_id):
    #     """Возвращает URL для загрузки аудио."""
    #     return f'upload/{obj_id}/'
    #
    # def get_urls(self):
    #     """Добавляем кастомный URL для обработки загрузки аудио."""
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('upload/<int:obj_id>/', self.admin_site.admin_view(self.upload_audio), name='upload_audio'),
    #     ]
    #     return custom_urls + urls
    #
    # def upload_audio(self, request, obj_id):
    #     """Обработчик загрузки аудио."""
    #     if request.method == 'POST':
    #         if not request.user.has_perm('iko.change_audionumber'):  # Проверка прав
    #             return HttpResponseForbidden()
    #         audio_file = request.FILES.get('audio_file')
    #         if audio_file:
    #             obj = AudioNumber.objects.get(id=obj_id)
    #             obj.audio = audio_file
    #             obj.save()
    #     return redirect('..')  # Возвращаемся на страницу списка