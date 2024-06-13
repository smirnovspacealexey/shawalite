from django.core.management.base import BaseCommand, CommandError
from shaw_queue.models import Menu, MenuCategory, ProductOption, ProductVariant, ContentOption, SizeOption, MacroProduct
from django.utils import timezone
from django.contrib.sessions.models import Session
import logging
import sys, traceback
import requests


logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('--------START---------')

        for item in Menu.objects.all():
            if item.menu_title == '':
                item.menu_title = item.title
                item.save()

        for item in MenuCategory.objects.all():
            if item.menu_title == '':
                item.menu_title = item.title
                item.save()

        for item in ProductOption.objects.all():
            if item.menu_title == '':
                item.menu_title = item.title
                item.save()

        for item in ProductVariant.objects.all():
            if item.menu_title == '':
                item.menu_title = item.title
                item.save()

        for item in ProductOption.objects.all():
            if item.menu_title == '':
                item.menu_title = item.title
                item.save()

        for item in ProductVariant.objects.all():
            if item.menu_title == '':
                item.menu_title = item.title
                item.save()

        for item in ContentOption.objects.all():
            if item.menu_title == '':
                item.menu_title = item.title
                item.save()

        for item in SizeOption.objects.all():
            if item.menu_title == '':
                item.menu_title = item.title
                item.save()

        for item in MacroProduct.objects.all():
            if item.menu_title == '':
                item.menu_title = item.title
                item.save()


        print('---------END----------')


