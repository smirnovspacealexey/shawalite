from django.utils import timezone
from django.db import models


class MangoSettings(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    test_phone = models.CharField(max_length=200, null=True, blank=True)
    vpbx_api_key = models.CharField(verbose_name='Уникальный код вашей АТС', max_length=200)
    vpbx_api_salt = models.CharField(verbose_name='Ключ для создания подписи', max_length=200)
    from_extension = models.CharField(verbose_name='Идентификатор сотрудника', max_length=10)
    active = models.BooleanField('active', default=True)

    def __str__(self):
        return self.name if self.name else f'id{self.pk}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.active:
            type(self).objects.exclude(pk=self.pk).update(active=False)
        super().save()

    @staticmethod
    def current():
        return MangoSettings.objects.filter(active=True).last()

    @staticmethod
    def tokens():
        current = MangoSettings.current()
        if current:
            return current.vpbx_api_key, current.vpbx_api_salt, current.from_extension
        else:
            return '', '', ''


class SMSHistory(models.Model):
    phone = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    date = models.DateTimeField('дата, время', default=timezone.now)
    success = models.BooleanField('success', default=False)
    result = models.CharField(max_length=200, null=True, blank=True)




