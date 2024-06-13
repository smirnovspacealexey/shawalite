from django.contrib import admin
from .models import YandexSettings, DeliveryHistory, DeliverySettings, DeliveryDistance, DeliveryActive
from time import gmtime, strftime


@admin.register(YandexSettings)
class YandexSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'token', 'active']
    list_editable = ('token', 'active')
    search_fields = ['__str__', ]


@admin.register(DeliveryHistory)
class DeliveryHistoryAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'six_numbers', 'daily_number', 'full_price', 'order', 'confirm', 'claim_id', 'status']
    list_editable = ('status',)
    raw_id_fields = ["order",]


@admin.register(DeliverySettings)
class DeliverySettingsAdmin(admin.ModelAdmin):
    search_fields = ['distances', 'active']
    filter_horizontal = ('distances', )


@admin.register(DeliveryDistance)
class DeliveryDistanceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'meters', 'roubles', 'menu_item']
    list_editable = ('meters', 'roubles', 'menu_item')
    search_fields = ['meters', 'roubles']


@admin.register(DeliveryActive)
class DeliveryActiveAdmin(admin.ModelAdmin):
    list_display = ['pk', 'delivery']




