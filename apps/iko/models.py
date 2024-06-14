from django.db import models
from django import forms
from django.utils import timezone


class iikoSettings(models.Model):
    url = models.CharField(max_length=200)
    active = models.BooleanField('active', default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.active:
            type(self).objects.exclude(pk=self.pk).update(active=False)
        super().save()

    @staticmethod
    def get_active():
        return iikoSettings.objects.filter(active=True).last()

