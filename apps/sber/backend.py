import requests
import json
import time
from django.urls import reverse, resolve

from shawarma.settings import HOST_SITE
from .models import SberSettings, SberTransaction


class Sber:
    def __init__(self):
        sber_settings = SberSettings.get_active()
        if sber_settings:
            self.login = sber_settings.login
            self.password = sber_settings.password
            self.min_amount = sber_settings.min_amount * 100
            self.max_amount = sber_settings.max_amount * 100
            self.tax_system = sber_settings.tax_system
            if sber_settings.in_test:
                self.host = 'https://secure-payment-gateway.ru/'
            else:
                self.host = 'https://securecardpayment.ru/'
            print(self.login, self.password)
        else:
            raise Exception('need SberSettings active object')

    def registrate_order(self, amount, order_id, ):
        order_id = str(time.time())[:-8] + '-' + order_id
        amount = int(amount) * 100
        if amount > self.max_amount:
            return False, f'Сумма заказа больше {self.max_amount/100}'
        if amount < self.min_amount:
            return False, f'Сумма заказа меньше {self.min_amount/100}'

        url = self.host + 'payment/rest/register.do'
        data = {
            "userName": self.login,
            "password": self.password,
            'amount': amount,
            'orderNumber': order_id,
            'taxSystem': self.tax_system,
            'returnUrl': HOST_SITE,
            'failUrl': HOST_SITE,
            # 'orderBundle': {"customerDetails": {"phone": "9888888888", "inn": "", "email": "email@mail.com"},
            #               "cartItems": {"items": [{"positionId": 1,
            #                                        "name": "Трость опорная, регулируемая по высоте, без устройства противоскольжения",
            #                                        "itemDetails": {"itemDetailsParams": [{"name": "fes_truCode",
            #                                                                               "value": "329921120.06001010100000000643"}]},
            #                                        "quantity": {"value": "3.00", "measure": "шт."},
            #                                        "itemCode": "270_235.00", "itemPrice": 40000,
            #                                        "tax": {"taxType": 0, "taxSum": 0}},
            #                                       {"positionId": 2, "name": "Трость белая тактильная цельная",
            #                                        "itemDetails": {"itemDetailsParams": [{"name": "fes_truCode",
            #                                                                               "value": "329921120.06002020100000000643"}]},
            #                                        "quantity": {"value": "3.00", "measure": "шт."},
            #                                        "itemCode": "270_244.00", "itemPrice": 23500,
            #                                        "tax": {"taxType": 0, "taxSum": 0}}]}}

            # 'returnUrl': HOST_SITE + reverse('successful_payment'),
            # 'failUrl': HOST_SITE + reverse('failed_payment'),

        }

        print(data)
        res = requests.post(url, data=data)
        if res.status_code == 200:
            response = json.loads(res.content.decode("utf-8"))
            SberTransaction.objects.create(orderNumber=order_id, data=str(data), accepted=True)
            return True, response
        else:
            SberTransaction.objects.create(orderNumber=order_id, data=str(res.status_code), accepted=False)
            return False, res.status_code

    def check_order_status(self, order_number=None, order_id=None):
        if not order_number and not order_id:
            return False, 'нужен order_number или order_id'
        url = self.host + 'payment/rest/getOrderStatusExtended.do'
        data = {
            "userName": self.login,
            "password": self.password,
            'orderNumber': order_number,
            'orderId': order_id,

        }
        print(data)
        res = requests.post(url, data=data)
        if res.status_code == 200:
            response = json.loads(res.content.decode("utf-8"))
            return True, response
        else:
            return False, res.status_code

