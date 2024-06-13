# -*- coding: utf-8 -*-
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.contrib.contenttypes.models import ContentType
import datetime
import logging
from django.utils.html import format_html
from apps.logs.models import Log


logger_debug = logging.getLogger('debug_logger')  # del me


# Create your models here.
class MenuCategory(models.Model):
    title = models.CharField(max_length=20)
    menu_title = models.CharField(max_length=200, default="", verbose_name="Название для меню")
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    eng_title = models.CharField(max_length=20)
    weight = models.IntegerField(verbose_name="Weight", default=0)
    hidden = models.BooleanField(default="False")
    customer_appropriate = models.BooleanField(verbose_name="Подходит для демонстрации покупателю", default=False)

    def __str__(self):
        return u"{}".format(self.title)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

        # def __unicode__(self):
        #     return "{}".format(self.title)


class StaffCategory(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return u"{}".format(self.title)

        # def __unicode__(self):
        #     return "{}".format(self.title)


class Server1C(models.Model):
    title = models.CharField(max_length=500, default="")
    ip_address = models.CharField(max_length=500, default="")
    port = models.CharField(max_length=500, default="")

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return "{}".format(self.title)


class ServicePoint(models.Model):
    title = models.CharField(max_length=100, default="")
    subnetwork = models.CharField(max_length=10, default="")
    server_1c = models.ForeignKey(Server1C, default=None, null=True, on_delete=models.CASCADE)
    latitude = models.FloatField(verbose_name="Широта", default=55.196829, blank=False, null=False)
    longitude = models.FloatField(verbose_name="Долгота", default=61.395762, blank=False, null=False)
    default_remote_order_acceptor = models.BooleanField(verbose_name="Точка, принимающая интернет-заказы",
                                                        default=False,
                                                        help_text="Может быть выбрана ТОЛЬКО ОДНА точка.")

    fullname = models.CharField('полное название', max_length=500, default="", blank=True,
                                help_text="С указанием города. Важно вводить населенный пункт с указанием номера дома,"
                                          " но без номера квартиры, подъезда, этажа")
    building = models.CharField('строение ', max_length=500, default="", help_text="Для доставки", blank=True)
    building_name = models.CharField('название апартаментов', max_length=500, default="", help_text="Для доставки", blank=True)
    city = models.CharField('город', max_length=500, default="", help_text="Для доставки", blank=True)
    country = models.CharField('страна', max_length=500, default="", help_text="Для доставки", blank=True)
    comment = models.CharField('комментарий по-умолчанию', max_length=500, default="", blank=True, help_text="Для доставки")
    description = models.CharField('описание', max_length=500, default="", blank=True,
                                   help_text="Для доставки, Географическая область, уточняющая до глобального соответствия")
    porch = models.CharField('подъезд', max_length=500, default="", help_text="Для доставки", blank=True)
    sflat = models.CharField('Квартира', max_length=500, default="", help_text="Для доставки", blank=True)
    sfloor = models.CharField('Этаж', max_length=500, default="1", help_text="Для доставки", blank=True)

    phone = models.CharField(max_length=200, default='',  help_text='Для доставки')

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return "{}".format(self.title)


class ServiceAreaPolygon(models.Model):
    service_point = models.ForeignKey(ServicePoint, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Название", max_length=25, default="Полигон", blank=False, null=False)
    note = models.CharField(verbose_name="Описание", max_length=200, blank=True)

    def __str__(self):
        return u"[{}] {}".format(self.service_point, self.title)


class ServiceAreaPolyCoord(models.Model):
    polygon = models.ForeignKey(ServiceAreaPolygon, on_delete=models.CASCADE)
    point_order = models.IntegerField(verbose_name="Порядок вершины",
                                      help_text="Вершины полигона должны быть перечислены в порядке правого обхода ("
                                                "по часовой стрелке).")
    latitude = models.FloatField(verbose_name="Широта", blank=False, null=False)
    longitude = models.FloatField(verbose_name="Долгота", blank=False, null=False)

    def __str__(self):
        return u"[{}] {}({} {})".format(self.polygon, self.point_order, self.longitude, self.latitude)


class Staff(models.Model):
    staff_category = models.ForeignKey(StaffCategory, on_delete=models.SET_NULL, null=True)
    available = models.BooleanField(default="False")
    fired = models.BooleanField(default="False")
    super_guy = models.BooleanField(default="False")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_point = models.ForeignKey(ServicePoint, default=None, null=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=20, verbose_name="телефон", default=None, null=True)

    def __str__(self):
        return u"{} {} {}".format(self.staff_category, self.user.first_name, self.user.last_name)

    def __unicode__(self):
        return "{} {} {}".format(self.staff_category, self.user.first_name, self.user.last_name)


class Menu(models.Model):
    title = models.CharField(max_length=200)
    menu_title = models.CharField(max_length=200, default="", verbose_name="Название для меню")
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    note = models.CharField(max_length=500, null=False)
    price = models.FloatField(default=0, validators=[MinValueValidator(0, "Price can't be negative!")])
    avg_preparation_time = models.DurationField(verbose_name="Average preparation time.")
    can_be_prepared_by = models.ForeignKey(StaffCategory, on_delete=models.SET_NULL, null=True)
    guid_1c = models.CharField(max_length=100, default="")
    category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True)
    is_by_weight = models.BooleanField(verbose_name="На развес", default=False)
    customer_appropriate = models.BooleanField(verbose_name="Подходит для демонстрации покупателю", default=False)
    icon = models.ImageField(upload_to="img/icons", blank=True, null=True, verbose_name="Иконка")
    QR_required = models.BooleanField(verbose_name="QR обязателен", default=False)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def js_price(self):
        return str(self.price).replace(',', '.')

    def get_cooking_time(self):
        try:
            cooking_times = self.cookingtime_set.all()
            if len(cooking_times) == 0:
                cooking_times = self.category.cookingtime_set.all()
                if len(cooking_times) == 0:
                    cooking_time = CookingTime.objects.filter(default=True).last()
                    if cooking_time:
                        return cooking_time.minutes
                    else:
                        return 15
            return cooking_times.order_by('minutes').last().minutes
        except:
            return 15

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return "{}".format(self.title)


class MacroProduct(models.Model):
    title = models.CharField(max_length=200)
    menu_title = models.CharField(max_length=200, default="", verbose_name="Название для меню")
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    icon = models.ImageField(upload_to="img/icons", blank=True, null=True, verbose_name="Иконка")
    hide = models.BooleanField(verbose_name="скрыть", default=False)
    ordering = models.IntegerField(verbose_name="ordering", default=0)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        return u"{}".format(self.title)

    class Meta:
        ordering = ('ordering',)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        same_ordering_macros = MacroProduct.objects.all().exclude(pk=self.pk).filter(ordering=self.ordering)
        if len(same_ordering_macros) > 0:
            ordering = self.ordering
            for same_ordering_macro in same_ordering_macros:
                ordering += 1
                same_ordering_macro.ordering = ordering
                same_ordering_macro.save()

        super().save()


class SizeOption(models.Model):
    title = models.CharField(max_length=200)
    menu_title = models.CharField(max_length=200, default="", verbose_name="Название для меню")
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        return u"{}".format(self.title)


class ContentOption(models.Model):
    title = models.CharField(max_length=200)
    menu_title = models.CharField(max_length=200, default="", verbose_name="Название для меню")
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        return u"{}".format(self.title)


class MacroProductContent(models.Model):
    """
    Шаурма со свининой, Говяжий шашлык, Coca-cola...
    """
    title = models.CharField(max_length=200)
    menu_title = models.CharField(max_length=200, default="", verbose_name="Название для меню")
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    picture = models.ImageField(upload_to="img/category_pictures", blank=True, null=True, verbose_name="Иконка")
    customer_appropriate = models.BooleanField(verbose_name="Подходит для демонстрации покупателю", default=False)
    content_option = models.ForeignKey(ContentOption, on_delete=models.CASCADE, verbose_name="Вариант содержимого",
                                       null=True)
    macro_product = models.ForeignKey(MacroProduct, on_delete=models.CASCADE, verbose_name="Макротовар", null=True)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        return u"{}".format(self.title) if bool(self.picture) else u"{} [No Photo]".format(self.title)


class ProductVariant(models.Model):
    title = models.CharField(max_length=200)
    menu_title = models.CharField(max_length=200, default="", verbose_name="Название для меню")
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Товар из меню 1С")
    size_option = models.ForeignKey(SizeOption, on_delete=models.CASCADE, verbose_name="Вариант размера")
    # content_option = models.ForeignKey(ContentOption, on_delete=models.CASCADE, verbose_name="Вариант содержимого")
    # macro_product = models.ForeignKey(MacroProduct, on_delete=models.CASCADE, verbose_name="Макротовар")
    macro_product_content = models.ForeignKey(MacroProductContent, on_delete=models.CASCADE,
                                              verbose_name="Содержимое макротовара", null=True)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        return u"{}".format(self.title)

    class Meta:
        ordering = ('title', 'customer_title')


class ProductOption(models.Model):
    title = models.CharField(max_length=200)
    menu_title = models.CharField(max_length=200, default="", verbose_name="Название для меню")
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Товар из меню 1С")
    product_variants = models.ManyToManyField(ProductVariant, verbose_name="Вариант товара")

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        return u"{}".format(self.title)


class Servery(models.Model):
    display_title = models.CharField(max_length=500, default="")
    title = models.CharField(max_length=500, default="")
    ip_address = models.CharField(max_length=500, default="")
    guid_1c = models.CharField(max_length=100, default="")
    service_point = models.ForeignKey(ServicePoint, default=None, null=True, blank=True, on_delete=models.CASCADE)
    payment_kiosk = models.BooleanField(verbose_name="Точка приёма платежей", default=True)
    default_remote_order_acceptor = models.BooleanField(verbose_name="Касса, принимающая интернет-заказы",
                                                        default=False,
                                                        help_text="Может быть выбрана ТОЛЬКО ОДНА касса на точку.")

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def __str__(self):
        if self.title:
            return u"{}".format(self.title)
        else:
            return 'no title'

    def __unicode__(self):
        return "{}".format(self.title)


class Order(models.Model):
    daily_number = models.IntegerField(verbose_name="Daily Number")
    delivery_daily_number = models.IntegerField(verbose_name="Delivery Daily Number", null=True, blank=True, default=None)
    open_time = models.DateTimeField(verbose_name="Open Time")
    close_time = models.DateTimeField(verbose_name="Close Time", blank=True, null=True)
    with_shawarma = models.BooleanField(verbose_name="With Shawarma", default=False)
    with_shashlyk = models.BooleanField(verbose_name="With Shashlyk", default=False)
    with_coffee = models.BooleanField(verbose_name="With Coffee", default=False)
    with_burger = models.BooleanField(verbose_name="With Burger", default=False)
    content_completed = models.BooleanField(verbose_name="Content Completed", default=False)
    shashlyk_completed = models.BooleanField(verbose_name="Shashlyk Completed", default=False)
    supplement_completed = models.BooleanField(verbose_name="Supplement Completed", default=False)
    coffee_completed = models.BooleanField(verbose_name="Coffee Completed", default=False)
    burger_completed = models.BooleanField(verbose_name="Burger Completed", default=False)
    start_shawarma_preparation = models.BooleanField(verbose_name="Start Shawarma Preparation", default=True)
    start_shawarma_cooking = models.BooleanField(verbose_name="Start Shawarma Cooking", default=True)
    # start_shashlyk_cooking = models.BooleanField(verbose_name="Start Shashlyk Cooking", default=True)
    total = models.FloatField(verbose_name="Сумма", default=0,
                              validators=[MinValueValidator(0, "Total can't be negative!")])
    discounted_total = models.FloatField(verbose_name="Сумма с учётом скидки", default=0,
                                         validators=[MinValueValidator(0, "Discounted total can't be negative!")])
    is_canceled = models.BooleanField(verbose_name="Is canceled", default=False)
    closed_by = models.ForeignKey(Staff, related_name="closer", verbose_name="Closed By", null=True,
                                  on_delete=models.SET_NULL)
    canceled_by = models.ForeignKey(Staff, related_name="canceler", verbose_name="Canceled By", null=True,
                                    on_delete=models.SET_NULL)
    opened_by = models.ForeignKey(Staff, related_name="opener", verbose_name="Opened By", null=True,
                                  on_delete=models.SET_NULL)
    prepared_by = models.ForeignKey(Staff, related_name="maker", default=None, null=True, on_delete=models.SET_NULL)
    printed = models.BooleanField(default=False, verbose_name="Check Printed")
    is_paid = models.BooleanField(default=False, verbose_name="Is Paid")
    is_grilling = models.BooleanField(default=False, verbose_name="Is Grilling")
    is_grilling_shash = models.BooleanField(default=False, verbose_name="Shashlyk Is Grilling")
    is_grilling_burger = models.BooleanField(default=False, verbose_name="Burger Is Grilling")
    is_preparing_coffee = models.BooleanField(default=False, verbose_name="Coffee Is Preparing")
    is_ready = models.BooleanField(default=False, verbose_name="Is Ready")
    is_voiced = models.BooleanField(default=False, verbose_name="Is Voiced")
    is_delivery = models.BooleanField(default=False, verbose_name="Is Delivery Order")
    is_preorder = models.BooleanField(default=False, verbose_name="Предзаказ")
    is_pickup = models.BooleanField(default=False, verbose_name="С собой")
    # True - if paid with cash, False - if paid with card.
    paid_with_cash = models.BooleanField(default=True, verbose_name="Paid With Cash")
    paid_with_sms = models.BooleanField(default=False, verbose_name="Paid With SMS")
    from_site = models.BooleanField(default=False, verbose_name="From site")
    pickup = models.BooleanField(default=False, verbose_name="Самовывоз")
    servery = models.ForeignKey(Servery, verbose_name="Servery", on_delete=models.CASCADE)
    guid_1c = models.CharField(max_length=100, default="")
    discount = models.FloatField(default=0, validators=[MinValueValidator(0, "Discount can't be negative!"),
                                                        MaxValueValidator(100, "Discount can't be greater then 100!")])
    sent_to_1c = models.BooleanField(verbose_name="Sent To 1C", default=False)
    paid_in_1c = models.BooleanField(verbose_name="Paid In 1C", default=False)
    status_1c = models.IntegerField(verbose_name="1C Status", default=200)

    def __str__(self):
        return u"{} №{}".format(self.servery, self.daily_number)

    def __unicode__(self):
        return "{} №{}".format(self.servery, self.daily_number)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.from_site:
            self.guid_1c = 'from_site'
        super().save()
        if self.delivery_daily_number and not self.deliveryhistory_set.last():
            from apps.delivery.models import DeliveryHistory

            delivery_history = DeliveryHistory.objects.filter(daily_number=str(self.delivery_daily_number)).last()
            if delivery_history and not delivery_history.order:
                delivery_history.order = self
                delivery_history.save()
                if delivery_history.paid:
                    self.is_paid = True
                    super().save()
                    from shaw_queue.views import send_order_to_1c
                    # Log.add_new(f'{self} models 362', '1C')
                    send_order_to_1c(self, False, paid=True)

    @property
    def display_number(self):
        delivery_order = self.deliveryorder_set.last()
        if self.from_site:
            return (str(delivery_order.daily_number) + 'C' if delivery_order else 'C') + str(self.daily_number % 100)
        elif self.delivery_daily_number:
            return 'Д' + str(self.delivery_daily_number)
        return str(self.daily_number % 100)

    class Meta:
        permissions = (
            ('can_cancel', 'User can cancel order.'),
            ('can_close', 'User can close order.'),
        )

    @property
    def six_numbers_for_yandex(self):
        delivery_history = self.deliveryhistory_set.last()
        if delivery_history:
            return delivery_history.six_numbers
        return '-'


class OrderContent(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Menu Item")
    staff_maker = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="Staff Maker", null=True)
    start_timestamp = models.DateTimeField(verbose_name="Start Timestamp", null=True)
    grill_timestamp = models.DateTimeField(verbose_name="Grill Start Timestamp", null=True)
    finish_timestamp = models.DateTimeField(verbose_name="Finish Timestamp", null=True)
    is_in_grill = models.BooleanField(verbose_name="Is in grill", default=False)
    is_canceled = models.BooleanField(verbose_name="Is canceled", default=False)
    canceled_by = models.ForeignKey(Staff, related_name="content_canceler", verbose_name="Canceled By", null=True,
                                    on_delete=models.SET_NULL)
    note = models.CharField(max_length=500, default="")
    qr = models.TextField(blank=True, null=True)
    quantity = models.FloatField(verbose_name="Quantity", default=1.0, null=False)

    def __str__(self):
        return u"№{} {}".format(self.order, self.menu_item)

    def __unicode__(self):
        return "№{} {}".format(self.order, self.menu_item)

    def info(self):
        html = f'''
        <span><b>Staff Maker:</b> {self.staff_maker}&nbsp; <b>Canceled By:</b> {self.canceled_by}<br/>
        <b>Start Timestam:</b> {self.start_timestamp.strftime("%B %d, %H:%M") if self.start_timestamp else '-'}&nbsp;
        <b>Grill Start Timestamp:</b> {self.grill_timestamp.strftime("%B %d, %H:%M") if self.grill_timestamp else '-'}
        <br/> <b>Finish Timestamp:</b> {self.finish_timestamp.strftime("%B %d, %H:%M") if self.finish_timestamp else '-'}<br/>
        <b>Is in grill:</b> {'✅' if self.is_in_grill else '❌'}&nbsp; <b>Is canceled:</b> {'✅' if self.is_canceled else '❌'}</span>
        <br/><br/>
        <b>Количество:</b> {int(self.quantity)}
        <br/><br/>
        <input hidden type="text" value="{self.menu_item}" id="menuitem-{self.pk}">    
        <b>пункут меню:</b>&nbsp;&nbsp;
        <i><a href="/admin/shaw_queue/menu/{self.menu_item.pk}/change/">{self.menu_item}</a></i>
        <br/>
        <br/>
        <a class="button" onclick="copyText('menuitem-{self.pk}')">копировать в буфер</a>
        '''
        if self.note:
            html += f'''
            <br/><br/><br/>
            <input hidden type="text" value="{self.note}" id="note-{self.pk}">
            <b>описание:</b>&nbsp;&nbsp;       
            <i>{self.note}</i>
            <br/>
            <br/>
            <a class="button" onclick="copyText('note-{self.pk}')">копировать в буфер</a><br/>
            '''
        else:
            html += '<br/><br/><b>без описания</b><br/>'

        if self.qr:
            html += f'''
            <br/><br/>
            <input hidden type="text" value="{self.note}" id="qr-{self.pk}">
            <b>QR:</b>&nbsp;&nbsp;       
            <i>{self.qr}</i>
            <br/>        
            <a class="button" onclick="copyText('qr-{self.pk}')">копировать в буфер</a><br/>
            '''
        else:
            html += '<br/><b>без qr</b><br/>'
        return format_html(html)

    info.allow_tags = False
    info.short_description = 'информация'

    class Meta:
        permissions = (
            ('can_cancel', 'User can cancel order content.'),
            ('can_cook', 'User can cook order content'),
        )


class OrderContentOption(models.Model):
    content_item = models.ForeignKey(OrderContent, on_delete=models.CASCADE, related_name="content_item",
                                     verbose_name="Товар из заказа")
    content_item_option = models.ForeignKey(OrderContent, on_delete=models.CASCADE, related_name="content_item_option",
                                            verbose_name="Доп к товару из заказа")

    def __str__(self):
        return u"{}-to-{}".format(self.content_item.menu_item.title, self.content_item_option.menu_item.title)


class OrderOpinion(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    mark = models.IntegerField(default=0)
    note = models.TextField(max_length=1000, blank=True, null=True)
    post_time = models.DateTimeField(verbose_name="Post Time", null=True)

    def __str__(self):
        return u"№{} {}".format(self.order, self.mark)

    def __unicode__(self):
        return "№{} {}".format(self.order, self.mark)


class PauseTracker(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    start_timestamp = models.DateTimeField(verbose_name="Start Timestamp", null=True)
    end_timestamp = models.DateTimeField(verbose_name="End Timestamp", null=True)

    class Meta:
        permissions = (
            ('view_statistics', 'User can view statistics pages.'),
        )


class Printer(models.Model):
    title = models.CharField(max_length=20, default="")
    ip_address = models.CharField(max_length=20, default="")
    service_point = models.ForeignKey(ServicePoint, default=None, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return u"№{} {}".format(self.title, self.service_point)

    def __unicode__(self):
        return "№{} {}".format(self.title, self.service_point)


class Customer(models.Model):
    name = models.CharField(max_length=30, default="Имя не указано", null=True, verbose_name="имя")
    phone_number = models.CharField(max_length=20, verbose_name="телефон")
    email = models.EmailField(blank=True, verbose_name="email")
    note = models.CharField(max_length=200, blank=True, verbose_name="комментарий")

    def __str__(self):
        return u"{} {}".format(self.phone_number, self.name)

    def __unicode__(self):
        return "{} {}".format(self.name, self.phone_number)

    def get_absolute_url(self):
        return reverse('customer-list')  # , kwargs={'pk': self.pk}


class DiscountCard(models.Model):
    number = models.CharField(max_length=30)
    discount = models.FloatField()
    guid_1c = models.CharField(max_length=100, default="")
    customer = models.ForeignKey(Customer, blank=True, null=True, verbose_name="owner of card",
                                 on_delete=models.CASCADE)

    def __str__(self):
        return u"№{} {}".format(self.number, self.customer)

    def __unicode__(self):
        return "№{} {}".format(self.number, self.customer)

    def get_absolute_url(self):
        return reverse('discount-card-list')  # , kwargs={'pk': self.pk}


class Delivery(models.Model):
    car_driver = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    departure_timepoint = models.DateTimeField(blank=True, null=True, verbose_name="время отправки")
    creation_timepoint = models.DateTimeField(verbose_name="время создания", default=timezone.now)
    daily_number = models.IntegerField(verbose_name="Daily Number", unique_for_date=datetime.date.today)
    is_canceled = models.BooleanField(verbose_name="Is canceled", default=False)
    is_finished = models.BooleanField(verbose_name="Is dinished", default=False)

    def __str__(self):
        return u"№{} {}".format(self.id, self.car_driver)

    def __unicode__(self):
        return "№{} {}".format(self.id, self.car_driver)

    def get_absolute_url(self):
        return reverse('delivery-list')  # , kwargs={'pk': self.pk}


def limit_order_choises_by_date():
    return {'open_time__gte': (timezone.now() - datetime.timedelta(days=2)).date()}


class DeliveryOrder(models.Model):
    CASH_PAYMENT = "CSH"
    CASHLESS_PAYMENT = "CLS"
    ONLINE_PAYMENT = "ONL"
    MIXED_PAYMENT = "MXD"
    PAYMENT_CHOISES = [
        (CASH_PAYMENT, 'Наличные'),
        (CASHLESS_PAYMENT, 'Безнал'),
        (ONLINE_PAYMENT, 'Сайт'),
        (MIXED_PAYMENT, 'Смешанная')]
    prefered_payment = models.CharField(max_length=3, choices=PAYMENT_CHOISES, default=ONLINE_PAYMENT,
                                        verbose_name="Вид оплаты")
    delivery = models.ForeignKey(Delivery, null=True, blank=True, verbose_name="доставка", on_delete=models.SET_NULL)
    daily_number = models.IntegerField(verbose_name="номер за день")  # , unique_for_date='obtain_timepoint'
    is_ready = models.BooleanField(default=False, verbose_name="готов к отправке")
    is_delivered = models.BooleanField(default=False, verbose_name="доставлен")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="включеный заказ",
                              limit_choices_to=limit_order_choises_by_date)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="клиент")
    address = models.CharField(max_length=250, default="Не указан", verbose_name="адрес")
    obtain_timepoint = models.DateTimeField(blank=True, null=True, verbose_name="время получения заказа")
    delivered_timepoint = models.DateTimeField(blank=True, null=True, verbose_name="время доставки заказа")
    prep_start_timepoint = models.DateTimeField(blank=True, null=True, verbose_name="время начала готовки")
    preparation_duration = models.DurationField(null=True, blank=True, default=datetime.timedelta(seconds=0),
                                                verbose_name="продолжительность готовки")
    delivery_duration = models.DurationField(null=True, blank=True, default=datetime.timedelta(seconds=0),
                                             verbose_name="продолжительность доставки")
    note = models.CharField(max_length=250, null=True, blank=True, help_text="Введите комментарий к заказу.",
                            verbose_name="комментарий")
    moderation_needed = models.BooleanField(default=False, verbose_name="требуется модерация")

    def __str__(self):
        return u"№{} {} {}".format(self.daily_number, self.customer.phone_number, self.order)

    def __unicode__(self):
        return "№{} {} {}".format(self.daily_number, self.customer.phone_number, self.order)

    def create_cooking_timer(self):
        max_minutes = 0
        first_cook = []
        last_cook = []
        order_content_all = self.order.ordercontent_set.all()
        for order_item in order_content_all:
            order_item_cooking_time = order_item.menu_item.get_cooking_time()
            logger_debug.info(f'create_cooking_timer {order_item} {order_item_cooking_time}')
            if max_minutes < order_item_cooking_time:
                max_minutes = order_item_cooking_time
                last_cook += first_cook
                first_cook = [order_item, ]
            elif max_minutes == order_item_cooking_time:
                first_cook.append(order_item)
            else:
                last_cook.append(order_item)

        for item in first_cook:
            CookingTimerOrderContent.cook_now(item)
        for item in last_cook:
            minutes = max_minutes - item.menu_item.get_cooking_time()
            date_time = timezone.now() + datetime.timedelta(minutes=minutes)
            CookingTimerOrderContent.objects.create(order_content=item, date_time=date_time)

    def get_absolute_url(self):
        return reverse('delivery-order-list')  # , kwargs={'pk': self.pk}


class CookingTimerOrderContent(models.Model):
    order_content = models.ForeignKey(OrderContent, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=True, null=True, verbose_name="время начала готовки")

    def __str__(self):
        return u"№{} {}".format(self.order_content, self.date_time)

    def cook_now(self=None, order_content=None):
        logger_debug.info(f'cook_now {order_content if order_content else self}')
        return


class CallData(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="customer who called")
    call_manager = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="manager who accepted call")
    ats_id = models.CharField(max_length=250, default="ID not set", unique=True)
    timepoint = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(null=True, blank=True, default=datetime.timedelta(seconds=0))
    record = models.CharField(max_length=256, default="Record path not set")
    accepted = models.BooleanField(default=False, verbose_name="Звонок принят")
    missed = models.BooleanField(default=False, verbose_name="Звонок пропущен")

    def __str__(self):
        return u"{} {}".format(self.customer, self.duration)

    def __unicode__(self):
        return "{} {}".format(self.customer, self.duration)

    def link(self):
        if self.record and self.record != 'Record path not set':
            return format_html(f'<a target=»_blank href="{self.record}">🔉</a>')
        else:
            return '🔇'

    def accepted_(self):
        yes = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
        no = '<img src="/static/admin/img/icon-no.svg" alt="True">'
        return format_html(f'{ yes if self.accepted else no}')

    def missed_(self):
        yes = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
        no = '<img src="/static/admin/img/icon-no.svg" alt="True">'
        return format_html(f'{ yes if self.missed else no}')

    # class Meta:
    #     ordering = ('-timepoint',)


class CookingTime(models.Model):
    minutes = models.IntegerField(verbose_name="минуты на готовку")
    products = models.ManyToManyField(Menu, verbose_name="Товары", blank=True)
    categories = models.ManyToManyField(MenuCategory, verbose_name="Категории", blank=True)
    default = models.BooleanField('по умолчанию', default=False)

    def __str__(self):
        return str(self.minutes)

    def __unicode__(self):
        return str(self.minutes)

    def quantity_products(self):
        return len(self.products.all())

    def quantity_categories(self):
        return len(self.categories.all())

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.default:
            type(self).objects.exclude(pk=self.pk).update(default=False)
        super().save()

