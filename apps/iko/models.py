from django.db import models
from django import forms
from django.utils import timezone
import datetime


class iikoSettings(models.Model):
    url = models.CharField(max_length=200)
    active = models.BooleanField('active', default=True)
    currenttoken = models.CharField(max_length=200, default='')
    last_update_token = models.CharField(max_length=200)
    last_update_token_live = models.IntegerField(verbose_name="время жизни тоенна в миллисекундах", default=1800000)
    last_getting = models.CharField(max_length=200)
    last_getting_live = models.IntegerField(verbose_name="время выжидания между запросами к iko", default=20000)
    orders = models.TextField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.active:
            type(self).objects.exclude(pk=self.pk).update(active=False)
        super().save()

    @staticmethod
    def get_active(idiko=None):
        if idiko:
            return iikoSettings.objects.filter(id=int(idiko)).last()
        else:
            return iikoSettings.objects.filter(active=True).last()

    @property
    def lat_token(self):
        seconds = int(self.last_update_token) / 1000.0
        dt = datetime.datetime.fromtimestamp(seconds)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def lat_req(self):
        seconds = int(self.last_getting) / 1000.0
        dt = datetime.datetime.fromtimestamp(seconds)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f'?iko={self.id}'


class IkoOrder(models.Model):
    ikoid = models.CharField(max_length=200, blank=True, null=True)
    number = models.CharField(max_length=200, blank=True, null=True)
    is_voiced = models.BooleanField(default=False, verbose_name="Is Voiced")
    datetime = models.DateTimeField('дата, время', default=timezone.now)

    def __str__(self):
        return f'{self.number} - {self.datetime}'


class AudioNumber(models.Model):
    name = models.CharField(max_length=200)
    audio = models.FileField(upload_to="audio", blank=True, null=True, verbose_name="audio")

    def __str__(self):
        return f'{self.pk} - {self.name}'

