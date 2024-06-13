from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from shaw_queue.models import Order, Staff, Menu, Servery
from shaw_queue.views import send_order_to_1c
from apps.delivery.backend import delivery_confirm
from apps.delivery.models import DeliveryHistory
from .models import SberTransaction
import logging
from random import sample
from django.views.decorators.csrf import csrf_exempt
import sys, traceback

logger_debug = logging.getLogger('debug_logger')


@csrf_exempt
def sber_result(request):
    daily_number = request.GET.get('daily_number')
    daily_number = daily_number[-6:]
    logger_debug.info(f'sber_result \n{request.GET}')
    try:
        if daily_number:
            transaction = SberTransaction.objects.filter(orderNumber=daily_number, paid=False, accepted=True,
                                                         date__contains=timezone.now().date()).last()
            if transaction:
                transaction.paid = True
                transaction.save()

            order = Order.objects.filter(open_time__contains=timezone.now().date(),
                                         close_time__isnull=True, is_canceled=False, is_paid=False,
                                         is_ready=False, is_delivery=True, delivery_daily_number=int(daily_number)).last()

            if order:
                order.is_paid = True
                order.save()
                data = send_order_to_1c(order, False, paid=True)
                # data = None
                delivery_history = order.deliveryhistory_set.last()

                logger_debug.info(f'sber_result order \n{order}\n {data}')
            else:
                delivery_history = DeliveryHistory.objects.filter(daily_number=daily_number, confirm=False).last()

            if delivery_history:  # доделать TODO
                delivery_history.paid = True
                delivery_history.save()
                if not delivery_history.wait_minutes:
                    delivery_confirm(delivery_history)
            else:  # доделать TODO
                order = Order.objects.filter(open_time__contains=timezone.now().date(),
                                             close_time__isnull=True, is_canceled=False, is_paid=False,
                                             is_ready=False, paid_with_sms=True,
                                             delivery_daily_number=int(daily_number)).last()
                if order:
                    order.is_paid = True
                    order.save()

        return JsonResponse(data={'success': True})
    except:
        logger_debug.info(f'sber_result ERROR: {traceback.format_exc()}')

#
# def add_cook_for_delivery_order(order):
#     has_cook_content = False
#     for item in order.ordercontent_set.all():
#         menu_item = item.menu_item
#         if menu_item.can_be_prepared_by.title == 'Cook':
#             has_cook_content = True
#             break
#     if has_cook_content:
#         try:
#             cooks = Staff.objects.filter(available=True, staff_category__title__iexact='Cook',
#                                          service_point=order.servery.service_point)
#             cooks = sample(list(cooks), len(cooks))
#         except:
#             logger_debug.info(f'add_coock ERROR: {traceback.format_exc()}')
#             return
#
#         if len(cooks) == 0:
#             logger_debug.info(f'add_coock ERROR: {traceback.format_exc()}')
#             return


