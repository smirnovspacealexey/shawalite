import requests
from .models import iikoSettings
from apps.logs.models import Log


def get_token():
    url = iikoSettings.get_active().url
    err = ''
    try:
        response = requests.get(url + 'login/2050')

        response.raise_for_status()

        data = response.json()
        print(data)

        iikoSettings.currenttoken = data
        iikoSettings.save()
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

    params = {"key": get_token()}
    iko = iikoSettings.get_active()
    url = iko.url
    response = requests.get(url + 'kitchenorders/', params=params)
    response.raise_for_status()

    data = response.json()
    print(data)
    Log.add_new(data, 'Iiko', title2='get_kitchenorders()')
    return data






