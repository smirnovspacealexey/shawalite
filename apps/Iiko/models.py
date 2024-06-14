# from django.db import models
# from django import forms
# from django.utils import timezone
#
#
# class iikoSettings(models.Model):
#     url = forms.CharField(widget=forms.PasswordInput())
#     active = models.BooleanField('active', default=True)
#
#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#         if self.active:
#             type(self).objects.exclude(pk=self.pk).update(active=False)
#         super().save()
#
