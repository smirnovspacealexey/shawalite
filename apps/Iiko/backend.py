import requests

url = 'https://example.com/api/resource'

params = {
    'param1': 'value1',
    'param2': 'value2'
}

# Заголовки запроса (если необходимо)
headers = {
    'Authorization': 'Bearer your_access_token',
    'Accept': 'application/json'
}

try:
    # Выполнение GET запроса
    response = requests.get(url, params=params, headers=headers)

    # Проверка статуса ответа
    response.raise_for_status()  # Вызывает исключение для статусов 4xx и 5xx

    # Обработка данных ответа (в формате JSON в данном примере)
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
