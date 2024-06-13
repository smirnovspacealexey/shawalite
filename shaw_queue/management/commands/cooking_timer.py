from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Order, Servery, DeliveryOrder, Customer, CookingTimerOrderContent
from django.utils import timezone
import logging

logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--------START---------')
        logger_debug.info(f'COOKING TIMER')
        for cooking_timer_item in CookingTimerOrderContent.objects.all():
            logger_debug.info(f'{cooking_timer_item}')
            logger_debug.info(f'{cooking_timer_item.date_time} {timezone.now()}')
            if cooking_timer_item.date_time < timezone.now():
                logger_debug.info(f'{cooking_timer_item} cook now!')
                cooking_timer_item.cook_now()

        print('---------END----------')
