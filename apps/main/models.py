from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models
import datetime


class ExcelBase(models.Model):
    name = models.CharField(max_length=200)
    excel = models.FileField(upload_to="excels", blank=True, null=True, verbose_name="excel")

    def __str__(self):
        return f'{self.pk} - {self.name}'


class PopularNote(models.Model):
    note = models.CharField(max_length=1000)
    position = models.IntegerField(verbose_name="position")

    def __str__(self):
        return f'{self.pk} - {self.note}'


class NoteBTN(models.Model):
    note = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to="img/notes/category_pictures", blank=True, null=True, verbose_name="Иконка")
    position = models.IntegerField(verbose_name="position")
    active = models.BooleanField('active', default=True)

    def __str__(self):
        return f'{self.pk} - {self.note}'

    class Meta:
        ordering = ('active', 'position', 'note')

    @staticmethod
    def btns():
        return NoteBTN.objects.filter(active=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        note_btn = NoteBTN.objects.filter(position=self.position).last()
        if note_btn:
            note_btn.position = self.position + 1
            note_btn.save()
        super().save()

