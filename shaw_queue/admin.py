# -*- coding: utf-8 -*-

from .models import Menu, Staff, Order, StaffCategory, \
    MenuCategory, Servery, ServicePoint, Printer, CallData, Customer, Delivery, DeliveryOrder, ServiceAreaPolygon, \
    ServiceAreaPolyCoord, MacroProduct, MacroProductContent, ProductOption, ProductVariant, SizeOption, ContentOption, \
    Server1C, CookingTime, OrderContent, CookingTimerOrderContent
from django.contrib import admin
from apps.delivery.backend import delivery_request
from django import forms


def accepted_everything(modeladmin, request, queryset):
    CallData.objects.filter(accepted=False).update(accepted=True)

accepted_everything.short_description = 'завершить все звонки'


def testdelivery(modeladmin, request, queryset):
    from apps.delivery.models import YandexSettings
    yandex_settings = YandexSettings.current()
    destination = {
        "fullname": "Челябинск, Университетская Набережная 63",
        "building": "63",
        "building_name": "",
        "city": "Челябинск",
        "comment": "ТЕСТОВЫЙ ЗАКАЗ НЕ ВЫПОЛНЯТЬ. ТЕСТИРУЕМ АПИ",
        "country": "Россия",
        "description": "Челябинск, Россия",
        "door_code": "",
        "door_code_extra": "",
        "doorbell_name": "",
        "porch": "1",
        "sflat": "1",
        "sfloor": "1",

        "email": '',
        "name": 'Alex',
        "phone": yandex_settings.test_phone,

    }
    order_content = OrderContent.objects.last()
    delivery_request(order_content.order, queryset.first(), destination)


testdelivery.short_description = 'сделать тестовый заказ'


# Register your models here.
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0

    # fieldsets = (
    #     (None, {
    #         # 'fields': ('menu_item', 'note', 'quantity', 'info'),
    #         'fields': ('title', ),
    #     }),
    # )
    readonly_fields = ('title',)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0

    # fieldsets = (
    #     (None, {
    #         'fields': ('title', 'customer_title'),
    #     }),
    # )
    # add_fieldsets = (
    #     (
    #         None,
    #         {"url": ("get_admin_url",), },
    #     ),
    # )
    readonly_fields = ('menu_item', 'size_option', 'macro_product_content',)
    show_change_link = True


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 0

    # fieldsets = (
    #     (None, {
    #         # 'fields': ('menu_item', 'note', 'quantity', 'info'),
    #         'fields': ('title', ),
    #     }),
    # )
    readonly_fields = ('title',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer_title', 'note', 'price', 'guid_1c', 'category', 'can_be_prepared_by', 'get_cooking_time', 'QR_required']
    search_fields = ['title', 'guid_1c', 'can_be_prepared_by__title', 'category__title']
    list_editable = ('customer_title', 'category', 'QR_required', 'can_be_prepared_by')
    inlines = [ProductVariantInline, ProductOptionInline]

    Menu.get_cooking_time.short_description = 'время готовки'


@admin.register(Servery)
class ServeryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'display_title', 'ip_address', 'guid_1c', 'service_point', 'payment_kiosk', 'default_remote_order_acceptor']
    search_fields = ['display_title', 'title', 'guid_1c', ]
    list_editable = ('ip_address', 'guid_1c', 'service_point', 'payment_kiosk', 'default_remote_order_acceptor')


@admin.register(CallData)
class CallDataAdmin(admin.ModelAdmin):
    list_display = ['customer', 'call_manager', 'ats_id', 'timepoint', 'accepted_', 'missed_', 'duration', 'link']
    search_fields = ['customer__phone_number', 'customer__name', 'customer__email', 'ats_id', ]
    list_filter = ['accepted', 'missed', ]
    actions = [accepted_everything, ]
    raw_id_fields = ['customer']
    CallData.accepted_.short_description = 'принят'
    CallData.missed_.short_description = 'пропущен'
    CallData.link.short_description = 'запись'


class OrderContentInline(admin.TabularInline):
    model = OrderContent
    extra = 0

    fieldsets = (
        (None, {
            # 'fields': ('menu_item', 'note', 'quantity', 'info'),
            'fields': ('info', ),
        }),
    )
    readonly_fields = ('info',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'daily_number', 'delivery_daily_number', 'open_time', 'close_time', 'content_completed', 'is_paid', 'is_ready', 'is_delivery', 'is_preorder', 'from_site', 'guid_1c']
    list_editable = ('daily_number', 'delivery_daily_number', 'close_time', 'is_paid', 'is_ready', 'is_delivery', 'content_completed')
    search_fields = ['daily_number', 'delivery_daily_number', 'open_time', 'guid_1c', 'servery__title']
    list_filter = ['from_site', 'is_delivery', 'is_paid', 'open_time', 'close_time', 'is_preorder']
    inlines = [OrderContentInline]


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer_title', 'menu_item',]
    search_fields = ['title', 'customer_title']
    filter_horizontal = ('product_variants', )


@admin.register(CookingTime)
class CookingTimeAdmin(admin.ModelAdmin):
    list_display = ['minutes', 'quantity_products', 'quantity_categories', 'default']
    list_editable = ('default', )
    search_fields = ['minutes', ]
    filter_horizontal = ()


@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ['order', 'daily_number', 'address', 'obtain_timepoint', 'note', 'moderation_needed', 'is_ready', 'is_delivered']
    list_editable = ('note', 'moderation_needed')
    search_fields = ['note', 'address']
    raw_id_fields = ["order", 'customer']


@admin.register(MacroProductContent)
class MacroProductContentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'menu_title', 'customer_title', 'customer_appropriate']
    list_editable = ('title', 'customer_appropriate')
    search_fields = ['title', 'menu_title', 'customer_title']


class MacroProductContentInline(admin.TabularInline):
    model = MacroProductContent
    extra = 0

    readonly_fields = ('content_option',)


@admin.register(MacroProduct)
class MacroProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'menu_title', 'customer_title', 'hide', 'icon', 'ordering']
    list_editable = ('title', 'icon', 'hide', 'ordering')
    search_fields = ['title', 'menu_title', 'customer_title']
    inlines = [MacroProductContentInline]


@admin.register(ServicePoint)
class ServicePointAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'fullname', 'latitude', 'longitude', 'subnetwork']
    list_editable = ('title', 'fullname', 'latitude', 'longitude', 'subnetwork')
    search_fields = ['title', 'fullname']
    actions = [testdelivery, ]


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'staff_category', 'available', 'fired', 'super_guy', 'service_point', 'phone_number']
    list_editable = ('staff_category', 'available', 'fired', 'super_guy', 'service_point', 'phone_number')
    search_fields = ['phone_number']
    list_filter = ['available', 'fired', 'super_guy', ]


admin.site.register(StaffCategory)
# admin.site.register(MenuCategory)
admin.site.register(Printer)
admin.site.register(Customer)
admin.site.register(Delivery)
admin.site.register(ServiceAreaPolygon)
admin.site.register(ServiceAreaPolyCoord)
# admin.site.register(ProductVariant)
# admin.site.register(SizeOption)
admin.site.register(ContentOption)
admin.site.register(Server1C)
admin.site.register(CookingTimerOrderContent)
# admin.site.register(OrderContent)


class MenuInline(admin.TabularInline):
    model = Menu
    extra = 0

    # fieldsets = (
    #     (None, {
    #         # 'fields': ('menu_item', 'note', 'quantity', 'info'),
    #         'fields': ('title', ),
    #     }),
    # )
    readonly_fields = ('title',)


@admin.register(SizeOption)
class SizeOptionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'customer_title', ]
    list_editable = ('title', 'customer_title',)
    search_fields = ['title', 'customer_title', ]
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'customer_title', 'menu_item', 'size_option', 'macro_product_content']
    list_editable = ('title', 'customer_title', 'size_option', )
    search_fields = ['title', 'customer_title', ]


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer_title', 'weight', 'hidden', 'customer_appropriate']
    list_editable = ('customer_title', 'weight', 'hidden', 'customer_appropriate')
    inlines = [MenuInline]


@admin.register(OrderContent)
class OrderContentAdmin(admin.ModelAdmin):
    list_display = ['order', 'start_timestamp', 'grill_timestamp', 'finish_timestamp', 'canceled_by']
    list_editable = ('start_timestamp', 'grill_timestamp', 'finish_timestamp', 'canceled_by')
    raw_id_fields = ['order', 'menu_item']
