from .models import DeliveryHistory, YandexSettings, DeliveryDistance, DeliveryActive
from shaw_queue.models import ServicePoint, Menu
import requests
import json
from apps.sms.backend import send_sms
import sys, traceback
import logging

logger_debug = logging.getLogger('debug_logger')
delivery_logger = logging.getLogger('delivery_logger')


url = 'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/'


def delivery_request(source, destination, history=None, order=None, order_items=None, price=None, items=None, wait_minutes=None):
    try:
        yandex_settings = YandexSettings.current()
        headers = {'Accept-Language': 'ru', 'Authorization': 'Bearer ' + yandex_settings.token}

        if not history:
            history = DeliveryHistory.objects.create(full_price=price)
            history.fullname = destination["fullname"]
            history.phone = destination['phone']
            history.longitude = destination['longitude']
            history.latitude = destination['latitude']
            history.city = destination['city']
            history.comment = destination['comment']
            history.country = destination['country']
            history.description = destination['description']
            history.door_code = destination.get('door_code', '')
            history.porch = destination.get('porch', '')
            history.sflat = destination.get('sflat', '')
            history.sfloor = destination.get('sfloor', '')
            history.wait_minutes = wait_minutes
            DeliveryActive.objects.create(delivery=history)

        cargo_options = []
        if yandex_settings.thermobag:
            cargo_options.append('thermobag')

        if yandex_settings.auto_courier:
            cargo_options.append('auto_courier')

        if not items:
            items = []

            for item in order_items:
                menu_item = Menu.objects.filter(pk=item['id']).last()

                if DeliveryDistance.objects.filter(menu_item=menu_item).exists():
                    continue

                if menu_item.customer_title:
                    title = menu_item.customer_title
                elif menu_item.title:
                    title = menu_item.title
                else:
                    continue
                items.append(
                    {
                        "cost_currency": yandex_settings.currency,
                        "cost_value": str(menu_item.price),
                        "droppof_point": 2,
                        "extra_id": str(item['id']),
                        "pickup_point": 1,
                        "quantity": item['quantity'],
                        "size": {
                            "height": 0.05,
                            "length": 0.1,
                            "width": 0.1
                        },
                        "title": title,
                        "weight": menu_item.category.weight / 1000
                    }
                )

        history.items = str(items)
        history.add_logg(str(destination), 'destination')

        data = {
            "client_requirements": {
                "assign_robot": yandex_settings.assign_robot,
                "pro_courier": yandex_settings.pro_courier,
                "taxi_class": yandex_settings.taxi_class,
                "cargo_options": cargo_options
            },
            "comment": "",
            "emergency_contact": {
                "name": source.title,
                "phone": source.phone
            },
            "items": items,
            "optional_return": yandex_settings.optional_return,
            "referral_source": yandex_settings.referral_source,
            "route_points": [
                {
                    "address": {
                        "coordinates": [
                            source.longitude,  # Longitude
                            source.latitude   # Latitude
                        ],
                        "fullname": source.fullname,
                        "building": source.building,
                        "building_name": source.building_name,
                        "city": source.city,
                        "comment": source.comment,
                        "country": source.country,
                        "description": source.description,
                        # "door_code": "169",
                        # "door_code_extra": "Код на вход во двор № 1234, код от апартаментов № 4321",
                        # "doorbell_name": "Волк",
                        "porch": source.porch,
                        "sflat": source.sflat,
                        "sfloor": source.sfloor
                    },
                    "contact": {
                        "email": yandex_settings.email,
                        "name": source.title,
                        "phone": source.phone
                    },
                    "external_order_cost": {
                        "currency": yandex_settings.currency,
                        "currency_sign": yandex_settings.currency_sign,
                        "value": str(price)
                    },
                    "external_order_id": history.daily_number,
                    "pickup_code": history.six_numbers,
                    "point_id": 1,
                    "skip_confirmation": yandex_settings.skip_confirmation,
                    "type": "source",
                    "visit_order": 1
                },
                {
                    "address": {
                        "coordinates": [
                            destination["longitude"],  # Longitude
                            destination["latitude"]   # Latitude
                        ],
                        "fullname": destination["fullname"],
                        # "building": destination["building"],
                        # "building_name": destination["building_name"],
                        "city": destination["city"],
                        "comment": destination["comment"],
                        "country": destination["country"],
                        "description": destination["description"],
                        "door_code": destination.get('door_code', ''),
                        # "door_code_extra": destination["door_code_extra"],
                        # "doorbell_name": destination["doorbell_name"],
                        "porch": destination.get('porch', ''),
                        "sflat": destination.get('sflat', ''),
                        "sfloor": destination.get('sfloor', '')
                    },
                    "contact": {
                        # "email": destination['email'],
                        "name": destination.get('name', ''),
                        "phone": destination['phone']
                    },
                    "external_order_cost": {
                        "currency": yandex_settings.currency,
                        "currency_sign": yandex_settings.currency_sign,
                        "value": str(price)
                    },
                    "external_order_id":  history.daily_number,
                    "point_id": 2,
                    "skip_confirmation": yandex_settings.skip_confirmation,
                    "type": "destination",
                    "visit_order": 2
                }
            ],
            "skip_act": yandex_settings.skip_act,
            "skip_client_notify": yandex_settings.skip_client_notify,
            "skip_door_to_door": yandex_settings.skip_door_to_door,
            "skip_emergency_notify": yandex_settings.skip_emergency_notify
        }

        if not wait_minutes:
            history.add_logg(str(data), 'request to yandex')
            res = requests.post(f'{url}create?request_id={history.request_id}', json=data, headers=headers)
            response = json.loads(res.content.decode("utf-8"))
            print(res.status_code)
            print(response)
            history.add_logg(str(res) + '\n' + str(response), 'yandex response')
            if res.status_code == 200:
                delivery_logger.info(f'delivery_request: SUCCESS {response}')
                history.claim_id = response['id']
                history.save()
                return history.daily_number, history.six_numbers
            else:
                history.save()
                delivery_logger.info(f'delivery_request ERROR: {res}')
                return None, None
        else:
            history.save()
            return history.daily_number, history.six_numbers
    except:
        logger_debug.info(f'delivery_request ERROR: {traceback.format_exc()}')
        return None, None

    # logger_debug.info(f'delivery_request {order, order.pk} \n\n{headers} \n {data} \n {res.status_code} \n {response}')


def delivery_confirm(history):
    try:
        yandex_settings = YandexSettings.current()
        headers = {'Accept-Language': 'ru', 'Authorization': 'Bearer ' + yandex_settings.token}

        data = {
            "version": 1
        }
        res = requests.post(f'{url}/accept?claim_id={history.claim_id}', json=data, headers=headers)

        if res.status_code == 200:
            history.confirm = True
            history.save()

        logger_debug.info(f'delivery_request res: {res}')
    except:
        logger_debug.info(f'confirm ERROR: {traceback.format_exc()}')


def check_delivery_status(history):
    try:
        yandex_settings = YandexSettings.current()
        headers = {'Accept-Language': 'ru', 'Authorization': 'Bearer ' + yandex_settings.token}

        data = {
            "version": 1
        }
        res = requests.post(f'{url}/info?claim_id={history.claim_id}', json=data, headers=headers)

        if res.status_code == 200:
            response = json.loads(res.content.decode("utf-8"))
            history.status = response['status']
            history.save()

        logger_debug.info(f'check_delivery_status res: {res}')
    except:
        logger_debug.info(f'confirm ERROR: {traceback.format_exc()}')

