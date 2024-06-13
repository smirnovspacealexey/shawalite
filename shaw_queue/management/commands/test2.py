from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Order, Servery, DeliveryOrder, Customer
from django.utils import timezone
from django.contrib.sessions.models import Session


class Command(BaseCommand):

    def handle(self, *args, **options):
       print('--------START---------')

       # order = Order.objects.create(
       #     daily_number=11,
       #     open_time=timezone.now(),
       #     with_shawarma=True,
       #     shashlyk_completed=True,
       #     supplement_completed=True,
       #     start_shawarma_preparation=True,
       #     start_shawarma_cooking=True,
       #     total=100,
       #     is_paid=True,
       #     pickup=True,
       #     # is_delivery=True,
       #     from_site=True,
       #     # is_grilling=True,
       #     servery=Servery.objects.first(),
       #
       # )
       # print(order)
       # print(DeliveryOrder.objects.create(order=order, daily_number=11, customer=Customer.objects.first()))

       # i = 1719873 - 1000
       # a = 0
       # soc = []
       # for n in range(i):
       #     try:
       #         soc.append(n)
       #         if a == 20:
       #             a = 0
       #             try:
       #               print(n, Order.objects.filter(pk__in=soc).delete())
       #             except:
       #                 soc = []
       #                 pass
       #             soc = []
       #         else:
       #             a += 1
       #     except:
       #         pass

       # print(Order.objects.all().delete())

       print('---------END----------')


