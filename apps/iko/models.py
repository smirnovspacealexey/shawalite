from django.db import models
from django import forms
from django.utils import timezone


class iikoSettings(models.Model):
    url = models.CharField(max_length=200)
    active = models.BooleanField('active', default=True)
    currenttoken = models.CharField(max_length=200, default='')
    last_getting = models.CharField(max_length=200)
    orders = models.TextField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.active:
            type(self).objects.exclude(pk=self.pk).update(active=False)
        super().save()

    @staticmethod
    def get_active():
        return iikoSettings.objects.filter(active=True).last()

    def __str__(self):
        return f'?iko={self.id}'


class IkoOrder(models.Model):
    ikoid = models.CharField(max_length=200, blank=True, null=True)
    number = models.CharField(max_length=200, blank=True, null=True)
    is_voiced = models.BooleanField(default=False, verbose_name="Is Voiced")
    datetime = models.DateTimeField('дата, время', default=timezone.now)

    def __str__(self):
        return f'{self.number} - {self.datetime}'