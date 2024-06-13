from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Order, Servery, DeliveryOrder, Customer, OrderContent
from django.utils import timezone
from django.contrib.sessions.models import Session


class Command(BaseCommand):

    def handle(self, *args, **options):
       print('--------START---------')

       order = Order.objects.create(
           daily_number=88,
           open_time=timezone.now(),
           with_shawarma=True,
           with_burger=True,
           shashlyk_completed=True,
           supplement_completed=True,
           start_shawarma_preparation=True,
           start_shawarma_cooking=True,
           total=100,
           is_paid=True,
           pickup=False,
           # is_delivery=True,
           from_site=False,
           # is_grilling=True,
           servery=Servery.objects.first(),

       )

       new_order_content = OrderContent(order=order, menu_item_id=425, note='444', quantity=1)
       new_order_content.save()
       new_order_content = OrderContent(order=order, menu_item_id=325, note='325', quantity=1)
       new_order_content.save()

       print('---------END----------')


