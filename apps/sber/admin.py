from django.contrib import admin
from .models import SberSettings, SberSettingsForm, SberTransaction


@admin.register(SberSettings)
class SberSettingsAdmin(admin.ModelAdmin):
    form = SberSettingsForm
    list_display = ['login', 'min_amount', 'max_amount', 'tax_system', 'in_test', 'callback_token', 'active']
    list_editable = ('active', 'min_amount', 'max_amount', 'in_test', 'callback_token', )


@admin.register(SberTransaction)
class SberTransactionAdmin(admin.ModelAdmin):
    list_display = ['orderNumber', 'data', 'response', 'accepted', 'paid', 'date']
    list_editable = ('paid',)

