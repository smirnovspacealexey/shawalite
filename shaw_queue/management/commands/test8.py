from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Order, Servery, DeliveryOrder, Customer, MacroProduct, MacroProductContent, SizeOption, ProductOption, ProductVariant
from django.utils import timezone
from django.contrib.sessions.models import Session
import logging
import sys, traceback
import requests


logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('--------START---------')


        macro_products = MacroProduct.objects.all().order_by('title')

        for macro_product in macro_products:
            for content_option in MacroProductContent.objects.filter(macro_product=macro_product).distinct():
                for size_option in SizeOption.objects.filter(productvariant__macro_product_content=content_option).distinct():
                    try:
                        ProductVariant.objects.get(macro_product_content=content_option, size_option=size_option)
                    except:
                        print(macro_product, content_option, size_option)
                        # print(traceback.format_exc())
                        print(ProductVariant.objects.filter(macro_product_content=content_option, size_option=size_option))
                        print('-\n')




        print('---------END----------')


