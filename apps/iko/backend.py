import requests
from .models import iikoSettings
from apps.logs.models import Log
from datetime import datetime
import json
import time


def get_token():
    iko = iikoSettings.get_active()
    url = iko.url
    err = ''
    try:
        response = requests.get(url + 'login/2050')

        response.raise_for_status()

        data = response.json()
        print(data)

        iko.currenttoken = data
        iko.save()
        Log.add_new(data, 'Iiko', title2='get_token()')
        return data

    except requests.exceptions.HTTPError as err:
        print(f'HTTP error occurred: {err}')  # Выводит ошибку HTTP
        Log.add_new(f'HTTP error occurred: {err}', 'Iiko', title2='get_token()')
    except requests.exceptions.ConnectionError as err:
        print(f'Connection error occurred: {err}')  # Выводит ошибку соединения
        Log.add_new(f'Connection error occurred: {err}', 'Iiko', title2='get_token()')
    except requests.exceptions.Timeout as err:
        print(f'Timeout error occurred: {err}')  # Выводит ошибку таймаута
        Log.add_new(f'Timeout error occurred: {err}', 'Iiko', title2='get_token()')
    except requests.exceptions.RequestException as err:
        print(f'Request error occurred: {err}')  # Выводит любую другую ошибку запроса
        Log.add_new(f'Request error occurred: {err}', 'Iiko', title2='get_token()')


def drop_token():
    iko = iikoSettings.get_active()
    url = iko.url
    response = requests.get(url + 'logout/' + iko.currenttoken)
    response.raise_for_status()
    data = response.json()
    print(data)
    Log.add_new(data, 'Iiko', title2='drop_token()')
    return data


def get_kitchenorders():
    drop_token()
    get_token()
    iko = iikoSettings.get_active()

    params = {"key": iko.currenttoken}

    url = iko.url
    response = requests.get(url + 'kitchenorders/', params=params)
    response.raise_for_status()

    data = response.json()
    print(data)
    # Log.add_new(data, 'Iiko', title2='get_kitchenorders()')


    return data


def pull_kitchenorders(idiko=None):
    iko = None
    if idiko:
        print(idiko)
        iko = iikoSettings.objects.filter(id=int(idiko)).last()
        iko.currenttoken = '22'
    if not iko:
        iko = iikoSettings.get_active()

    current_mill = round(time.time() * 1000)
    # Log.add_new(str(current_mill) + ' ' + str(iko.last_getting), 'Iiko', title2='drop_token()')

    if current_mill - int(iko.last_getting) > 20000:
        iko.last_getting = current_mill
        data = get_kitchenorders()
        iko.orders = data
        iko.save()
    else:
        data = json.loads(iko.orders)


    try:
        current_date = datetime.now().date()
        # Log.add_new(str(data), 'Iiko', title2='new_data')
        for order in data:
             if "Items" in order:
                order["Items"] = [
                        item for item in order["Items"]
                        if item["PrintTime"] and datetime.fromisoformat(item["PrintTime"].split("T")[0]).date() == current_date
                    ]

        data = [order for order in data if order["Items"]]

        # Log.add_new(str(data), 'Iiko', title2='new_data')

        wait_orders = data.copy()
        ready_orders = data.copy()

        wait_orders = [
            order for order in wait_orders
            if any(item['ProcessingCompleteTime'] is None for item in order['Items']) and all(item['ProcessingStatus'] in {0, 1, 2, 3, 4} for item in order['Items']) and all(item['ServeTime'] is None for item in order['Items'])
        ]

        # wait_orders = [order for order in wait_orders if order["Items"]]

        ready_orders = [
            order for order in ready_orders
            if all(item['ProcessingCompleteTime'] is not None for item in order['Items']) and all(item['ProcessingStatus'] in {5, 6} for item in order['Items']) and all(item['ServeTime'] is None for item in order['Items'])
        ]

        # Log.add_new(str(ready_orders), 'Iiko', title2='ready_orders')

        return wait_orders, ready_orders

    except Exception as e:
        Log.add_new(str(e), 'Iiko', title2='error 1')
        return None




def filter_items(items):
    current_date = datetime.now().date()

    filtered_items = []
    for item in items:
        serve_time = item.get("ServeTime")

        # Проверим, существует ли ServeTime и отличается ли он от текущей даты
        if serve_time is not None:
            try:
                serve_time_date = datetime.strptime(serve_time,
                                                    "%Y-%m-%dT%H:%M:%S.%f%z").date()  # Формат времени в вашем JSON

                Log.add_new(str(serve_time_date) + '   ' + str(current_date), 'Iiko', title2='current_date')

                if serve_time_date == current_date:
                    filtered_items.append(item)
            except ValueError:
                pass  # Пропустим запись, если формат строки ServeTime не соответствует ожидаемому


    return filtered_items




