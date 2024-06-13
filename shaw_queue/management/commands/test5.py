from django.core.management.base import BaseCommand, CommandError
from apps.delivery.models import DeliveryHistory


class Command(BaseCommand):
    def handle(self, *args, **options):
        for dh in DeliveryHistory.objects.all():
            dh.status = 'delivered'
            dh.save()
