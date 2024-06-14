import requests

url = 'http://192.168.20.110:9042/api/'


def get_token():
    try:
        response = requests.get(url + 'login/2050')

        response.raise_for_status()

        data = response.json()
        print(data)

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Выводит ошибку HTTP
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')  # Выводит ошибку соединения
    except requests.exceptions.Timeout as timeout_err:
        print(f'Timeout error occurred: {timeout_err}')  # Выводит ошибку таймаута
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')  # Выводит любую другую ошибку запроса





