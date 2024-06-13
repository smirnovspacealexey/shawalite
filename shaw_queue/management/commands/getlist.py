from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Order, Servery, DeliveryOrder, Customer
from django.utils import timezone
from django.contrib.sessions.models import Session
import logging
import sys, traceback
import requests


logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('--------START---------')
        orders = Order.objects.filter(open_time__contains=timezone.now().date(),
                                      servery__service_point__subnetwork='24').order_by('open_time')

        total = ''
        for order in orders:
            print(order)
            content = order.ordercontent_set.filter(menu_item__can_be_prepared_by__title__in=['Barista', 'Burgerman']).first()
            if content:
                total += f'\n{content.menu_item.title} - #{order.pk}\n'
                print(f'\n\n{content.menu_item.title} - #{order.pk}\n\n')
        print(total)
        print('--------END---------')



