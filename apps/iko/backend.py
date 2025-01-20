import requests
from .models import iikoSettings
from apps.logs.models import Log
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
    Log.add_new(data, 'Iiko', title2='get_kitchenorders()')
    return data


def pull_kitchenorders():
    iko = iikoSettings.get_active()
    current_mill = round(time.time() * 1000)
    Log.add_new(str(current_mill) + ' ' + str(iko.last_getting), 'Iiko', title2='drop_token()')

    if current_mill - int(iko.last_getting) > 20000:
        iko.last_getting = current_mill
        iko.save()

        data = get_kitchenorders()

        new_data = []

        for item in data:
            filtered_data = filter_items(item["Items"])
            if filtered_data:
                new_data.append(item)

        return new_data

    return None


from datetime import datetime


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

                if serve_time_date == current_date:
                    filtered_items.append(item)
            except ValueError:
                pass  # Пропустим запись, если формат строки ServeTime не соответствует ожидаемому


    return filtered_items




