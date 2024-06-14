import requests
from .models import iikoSettings


def get_token():
    url = iikoSettings.get_active().url
    try:
        response = requests.get(url + 'login/2050')

        response.raise_for_status()

        data = response.json()
        print(data)

        iikoSettings.currenttoken = data
        iikoSettings.save()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Выводит ошибку HTTP
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')  # Выводит ошибку соединения
    except requests.exceptions.Timeout as timeout_err:
        print(f'Timeout error occurred: {timeout_err}')  # Выводит ошибку таймаута
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')  # Выводит любую другую ошибку запроса


def drop_token():
    iko = iikoSettings.get_active()
    url = iko.url
    response = requests.get(url + 'logout/' + iko.currenttoken)
    response.raise_for_status()
    data = response.json()
    print(data)
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
    return data






