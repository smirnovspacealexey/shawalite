from django.core.management.base import BaseCommand
from apps.iko.backend import get_token, get_kitchenorders


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('--------iiko---------')
        get_token()
        get_kitchenorders()
        print('---------------------')



