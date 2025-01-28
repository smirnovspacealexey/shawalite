import requests
from .models import iikoSettings
from apps.logs.models import Log
from datetime import datetime
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

    return [{
  'Id': '24953994-3602-460c-bdad-2ceb1e306171',
  'Number': 23,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '28bc5399-6037-41ac-a317-6a291b37b283',
    'Amount': 2.0,
    'ProductName': 'Шаурма Свинина сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:31:49.5619262+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:31:49.5739976+05:00',
    'Processing1BeginTime': '2025-01-28T12:39:42.7580264+05:00',
    'Processing2BeginTime': '2025-01-28T12:39:42.7580264+05:00',
    'Processing3BeginTime': '2025-01-28T12:42:13.9931468+05:00',
    'Processing4BeginTime': '2025-01-28T12:42:14.3700186+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:42:14.7778638+05:00',
    'ServeTime': '2025-01-28T12:42:31.7882832+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00818',
      'Amount': 2.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/d7505167-b8c9-4bf9-bafb-41029d99d370',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/23'
}, {
  'Id': '6b30c664-4559-465c-b11f-b1ea590ad308',
  'Number': 21,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'a644f2bb-c9b7-440b-aeff-4ec13c0f036a',
    'Amount': 1.0,
    'ProductName': 'Шаурма с индейкой мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:30:28.3150776+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:30:28.3265342+05:00',
    'Processing1BeginTime': '2025-01-28T12:32:45.8096494+05:00',
    'Processing2BeginTime': '2025-01-28T12:32:45.8096494+05:00',
    'Processing3BeginTime': '2025-01-28T12:40:23.2812947+05:00',
    'Processing4BeginTime': '2025-01-28T12:40:24.130694+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:40:24.7504084+05:00',
    'ServeTime': '2025-01-28T12:41:09.6255703+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00824',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/ff5f890e-2ab4-440d-88ba-2723278ec826',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/21'
}, {
  'Id': 'c4287641-9a28-436a-9939-f2a06c2cf5c7',
  'Number': 22,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '022a141e-0c6d-4150-82a4-82f00854f177',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:29:56.4300771+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:29:56.4497714+05:00',
    'Processing1BeginTime': '2025-01-28T12:32:43.7233561+05:00',
    'Processing2BeginTime': '2025-01-28T12:32:43.7233561+05:00',
    'Processing3BeginTime': '2025-01-28T12:40:25.6586609+05:00',
    'Processing4BeginTime': '2025-01-28T12:40:26.018467+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:40:26.3905383+05:00',
    'ServeTime': '2025-01-28T12:45:39.0934314+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/bd413059-faf1-4799-bc8a-8f605ed1036f',
  'OrderType': 'Доставка самовывоз',
  'OrderServiceType': 2,
  'IsDeliverySelfService': True,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/22'
}, {
  'Id': 'b82b16ae-dc84-483f-b0a6-733fc4246ddd',
  'Number': 20,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '5fe1af24-3849-4800-b696-018692e09f76',
    'Amount': 1.0,
    'ProductName': 'Морс в ассотрименте 0,5л',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:24:21.428531+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:24:21.428531+05:00',
    'Processing1BeginTime': '2025-01-28T12:25:15.3627171+05:00',
    'Processing2BeginTime': '2025-01-28T12:25:15.3627171+05:00',
    'Processing3BeginTime': '2025-01-28T12:25:15.997865+05:00',
    'Processing4BeginTime': '2025-01-28T12:25:15.997865+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:25:16.5944754+05:00',
    'ServeTime': '2025-01-28T12:25:17.2590222+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0,5л',
      'KitchenName': '0,5л'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '22653c4f-5494-496c-86f2-5d28e32331f4',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Клюква',
      'Product': 'http://192.168.24.28:9042/api/products/01711',
      'KitchenName': 'Выдача',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:24:21.428531+05:00',
      'Processing1BeginTime': '2025-01-28T12:25:15.3627171+05:00',
      'Processing2BeginTime': '2025-01-28T12:25:15.3627171+05:00',
      'Processing3BeginTime': '2025-01-28T12:25:15.997865+05:00',
      'Processing4BeginTime': '2025-01-28T12:25:15.997865+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:25:16.5944754+05:00',
      'ServeTime': '2025-01-28T12:25:17.2590222+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00945',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Морс',
      'AllowProductsCombining': False,
      'Scale': 'Напитки'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/c3ac4c24-6eb9-4609-8baf-7bbf84e76aed',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/20'
}, {
  'Id': '42f57a7f-5b2e-428c-982e-e9cc2fb37980',
  'Number': 19,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'ff082281-3282-4b98-ac4b-d87e1065de90',
    'Amount': 2.0,
    'ProductName': 'Шаурма Свинина сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:22:46.1414839+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:22:46.1571316+05:00',
    'Processing1BeginTime': '2025-01-28T12:25:11.5007921+05:00',
    'Processing2BeginTime': '2025-01-28T12:25:11.5007921+05:00',
    'Processing3BeginTime': '2025-01-28T12:40:33.3781858+05:00',
    'Processing4BeginTime': '2025-01-28T12:40:33.3781858+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:40:34.0323087+05:00',
    'ServeTime': '2025-01-28T12:40:34.9684953+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '80b373b3-8e6c-45b3-afb5-b8955e5b0b95',
      'Amount': 4.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Моцарелла',
      'Product': 'http://192.168.24.28:9042/api/products/01745',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:22:46.1571316+05:00',
      'Processing1BeginTime': '2025-01-28T12:25:11.5007921+05:00',
      'Processing2BeginTime': '2025-01-28T12:25:11.5007921+05:00',
      'Processing3BeginTime': '2025-01-28T12:40:33.3781858+05:00',
      'Processing4BeginTime': '2025-01-28T12:40:33.3781858+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:40:34.0323087+05:00',
      'ServeTime': '2025-01-28T12:40:34.9684953+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00818',
      'Amount': 2.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': '6b5cc0be-af23-40d1-82c7-0d8118a8eec1',
    'Amount': 1.0,
    'ProductName': 'Морс в ассотрименте 0,3л',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:22:46.1414839+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:22:46.1571316+05:00',
    'Processing1BeginTime': '2025-01-28T12:40:33.3781858+05:00',
    'Processing2BeginTime': '2025-01-28T12:40:33.3781858+05:00',
    'Processing3BeginTime': '2025-01-28T12:40:33.3781858+05:00',
    'Processing4BeginTime': '2025-01-28T12:40:33.3781858+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:40:34.0323087+05:00',
    'ServeTime': '2025-01-28T12:40:34.9684953+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0,3л',
      'KitchenName': '0,3л'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '8bdf5ac9-dbab-4515-a3c9-b7bf97d6a443',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Облепиха',
      'Product': 'http://192.168.24.28:9042/api/products/01713',
      'KitchenName': 'Выдача',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:22:46.1571316+05:00',
      'Processing1BeginTime': '2025-01-28T12:40:33.3781858+05:00',
      'Processing2BeginTime': '2025-01-28T12:40:33.3781858+05:00',
      'Processing3BeginTime': '2025-01-28T12:40:33.3781858+05:00',
      'Processing4BeginTime': '2025-01-28T12:40:33.3781858+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:40:34.0323087+05:00',
      'ServeTime': '2025-01-28T12:40:34.9684953+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00945',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Морс',
      'AllowProductsCombining': False,
      'Scale': 'Напитки'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/23cfa8f7-5077-40b4-a305-ffcd1a79ac0d',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/19'
}, {
  'Id': '3c89fb64-7d02-4b81-b436-61495029b87e',
  'Number': 134,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'c192639e-b008-4d74-89d2-448654bcbfa6',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': True,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-23T19:18:47.493+05:00',
    'EstimatedCookingBeginTime': '2025-01-23T19:18:47.517+05:00',
    'Processing1BeginTime': '2025-01-23T19:27:30.849+05:00',
    'Processing2BeginTime': '2025-01-23T19:27:30.849+05:00',
    'Processing3BeginTime': '2025-01-23T19:34:15.696+05:00',
    'Processing4BeginTime': '2025-01-23T19:34:15.696+05:00',
    'ProcessingCompleteTime': '2025-01-23T19:37:18.885+05:00',
    'ServeTime': '2025-01-23T21:26:05.702+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': '80ce5b1e-6799-4305-a646-a3cc828987de',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': True,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-23T19:18:47.493+05:00',
    'EstimatedCookingBeginTime': '2025-01-23T19:18:47.517+05:00',
    'Processing1BeginTime': '2025-01-23T19:27:25.466+05:00',
    'Processing2BeginTime': '2025-01-23T19:27:25.466+05:00',
    'Processing3BeginTime': '2025-01-23T19:34:17.946+05:00',
    'Processing4BeginTime': '2025-01-23T19:34:17.946+05:00',
    'ProcessingCompleteTime': '2025-01-23T19:37:18.885+05:00',
    'ServeTime': '2025-01-23T21:26:05.702+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': 'bc4dc67e-a860-46af-8f28-1bc478bf5c3c',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица большая',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': True,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-23T19:18:47.493+05:00',
    'EstimatedCookingBeginTime': '2025-01-23T19:18:47.517+05:00',
    'Processing1BeginTime': '2025-01-23T19:27:23.531+05:00',
    'Processing2BeginTime': '2025-01-23T19:27:23.531+05:00',
    'Processing3BeginTime': '2025-01-23T19:34:20.296+05:00',
    'Processing4BeginTime': '2025-01-23T19:34:20.296+05:00',
    'ProcessingCompleteTime': '2025-01-23T19:37:18.885+05:00',
    'ServeTime': '2025-01-23T21:26:05.702+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'большая',
      'KitchenName': 'большая'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/c176de06-a6a6-4144-a744-74399794320c',
  'OrderType': 'Доставка самовывоз',
  'OrderServiceType': 2,
  'IsDeliverySelfService': True,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/134'
}, {
  'Id': '2e8f8cd7-e8cf-4a89-aa58-d150eb9d01a4',
  'Number': 18,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '543b5c47-08c8-46d7-89a3-43cd1f918ebf',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:21:39.7211851+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:21:39.7368062+05:00',
    'Processing1BeginTime': '2025-01-28T12:22:21.9126852+05:00',
    'Processing2BeginTime': '2025-01-28T12:22:21.9126852+05:00',
    'Processing3BeginTime': '2025-01-28T12:33:09.8064816+05:00',
    'Processing4BeginTime': '2025-01-28T12:33:09.8064816+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:33:10.9231755+05:00',
    'ServeTime': '2025-01-28T12:33:47.3151528+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': '46595d8b-0c1f-46aa-a988-55798c354eca',
    'Amount': 1.0,
    'ProductName': 'Смузи в ассортименте 0,5л',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': True,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:21:39.7211851+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:21:39.7368062+05:00',
    'Processing1BeginTime': None,
    'Processing2BeginTime': None,
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 0,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0,5л',
      'KitchenName': '0,5л'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': 'f42ed9cb-7898-408e-b9b8-83ce106ce3d1',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Малина',
      'Product': 'http://192.168.24.28:9042/api/products/01716',
      'KitchenName': 'Выдача',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
      'Deleted': True,
      'EstimatedCookingBeginTime': '2025-01-28T12:21:39.7368062+05:00',
      'Processing1BeginTime': None,
      'Processing2BeginTime': None,
      'Processing3BeginTime': None,
      'Processing4BeginTime': None,
      'ProcessingCompleteTime': None,
      'ServeTime': None,
      'ProcessingStatus': 0,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01718',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Смузи',
      'AllowProductsCombining': False,
      'Scale': 'Напитки'
    }
  }, {
    'Id': '2e0da0f1-eac6-4475-a264-2fa7da48a020',
    'Amount': 1.0,
    'ProductName': 'Смузи в ассортименте 0,3л',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 3,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:21:52.1206461+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:21:52.1206461+05:00',
    'Processing1BeginTime': '2025-01-28T12:33:09.8064816+05:00',
    'Processing2BeginTime': '2025-01-28T12:33:09.8064816+05:00',
    'Processing3BeginTime': '2025-01-28T12:33:09.8064816+05:00',
    'Processing4BeginTime': '2025-01-28T12:33:09.8064816+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:33:10.9231755+05:00',
    'ServeTime': '2025-01-28T12:33:47.3151528+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0,3л',
      'KitchenName': '0,3л'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '35791168-43e6-4f2b-a13b-8dfa9e48a112',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Малина',
      'Product': 'http://192.168.24.28:9042/api/products/01716',
      'KitchenName': 'Выдача',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:21:52.1206461+05:00',
      'Processing1BeginTime': '2025-01-28T12:33:09.8064816+05:00',
      'Processing2BeginTime': '2025-01-28T12:33:09.8064816+05:00',
      'Processing3BeginTime': '2025-01-28T12:33:09.8064816+05:00',
      'Processing4BeginTime': '2025-01-28T12:33:09.8064816+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:33:10.9231755+05:00',
      'ServeTime': '2025-01-28T12:33:47.3151528+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01718',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Смузи',
      'AllowProductsCombining': False,
      'Scale': 'Напитки'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/4459d1dd-d7aa-4e6b-be09-e0ff4437e144',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/18'
}, {
  'Id': 'f7534667-a675-44af-a29e-c7ecabfeb8b6',
  'Number': 16,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '24436327-c26c-4e40-99ff-8528f667a245',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:17:27.8215513+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:17:27.8338582+05:00',
    'Processing1BeginTime': '2025-01-28T12:21:19.4909099+05:00',
    'Processing2BeginTime': '2025-01-28T12:21:19.4909099+05:00',
    'Processing3BeginTime': '2025-01-28T12:28:09.9452371+05:00',
    'Processing4BeginTime': '2025-01-28T12:28:10.3858772+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:28:10.9186452+05:00',
    'ServeTime': '2025-01-28T12:28:12.0598351+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': 'd6cb887a-5136-4841-9462-6db13387a291',
    'Amount': 1.0,
    'ProductName': 'Шаурма Свинина большая',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:17:27.8215513+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:17:27.8338582+05:00',
    'Processing1BeginTime': '2025-01-28T12:21:21.3330596+05:00',
    'Processing2BeginTime': '2025-01-28T12:21:21.3330596+05:00',
    'Processing3BeginTime': '2025-01-28T12:28:09.9452371+05:00',
    'Processing4BeginTime': '2025-01-28T12:28:10.3858772+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:28:10.9186452+05:00',
    'ServeTime': '2025-01-28T12:28:12.0598351+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'большая',
      'KitchenName': 'большая'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00818',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/1237bc52-ffac-45a3-916b-b64c25eb06b2',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/16'
}, {
  'Id': '96903071-ff58-460f-9e0e-9c795204239e',
  'Number': 15,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '9dfee24b-1337-47ca-9d57-e246b2bd355c',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': True,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:14:06.7360253+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:14:06.751839+05:00',
    'Processing1BeginTime': None,
    'Processing2BeginTime': None,
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 0,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': 'a049afe7-0f46-415a-9957-e334dda605fa',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Без красного',
      'Product': 'http://192.168.24.28:9042/api/products/01733',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': True,
      'EstimatedCookingBeginTime': '2025-01-28T12:14:06.751839+05:00',
      'Processing1BeginTime': None,
      'Processing2BeginTime': None,
      'Processing3BeginTime': None,
      'Processing4BeginTime': None,
      'ProcessingCompleteTime': None,
      'ServeTime': None,
      'ProcessingStatus': 0,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': 'ac8ef016-da3a-494f-aff6-b73dac58a04f',
    'Amount': 1.0,
    'ProductName': 'Капучино 0.3',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:14:06.7360253+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:14:06.751839+05:00',
    'Processing1BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'Processing2BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'Processing3BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'Processing4BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:33:13.3045875+05:00',
    'ServeTime': '2025-01-28T12:33:14.2882186+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0.3',
      'KitchenName': '0.3'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01299',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Кофе',
      'AllowProductsCombining': False,
      'Scale': 'Кофе'
    }
  }, {
    'Id': '3b9bf92d-38b5-4c77-aad8-87d3c9793507',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 3,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:14:20.4592163+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:14:20.4748107+05:00',
    'Processing1BeginTime': '2025-01-28T12:18:16.8751141+05:00',
    'Processing2BeginTime': '2025-01-28T12:18:16.8751141+05:00',
    'Processing3BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'Processing4BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:33:13.3045875+05:00',
    'ServeTime': '2025-01-28T12:33:14.2882186+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': 'f60f6ffa-c952-4d08-a103-8a69758d5855',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Без красного',
      'Product': 'http://192.168.24.28:9042/api/products/01733',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:14:20.4748107+05:00',
      'Processing1BeginTime': '2025-01-28T12:18:16.8751141+05:00',
      'Processing2BeginTime': '2025-01-28T12:18:16.8751141+05:00',
      'Processing3BeginTime': '2025-01-28T12:33:12.7551857+05:00',
      'Processing4BeginTime': '2025-01-28T12:33:12.7551857+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:33:13.3045875+05:00',
      'ServeTime': '2025-01-28T12:33:14.2882186+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }, {
      'Id': '63564c3a-962e-452f-8df0-03d074947b17',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Без лука',
      'Product': 'http://192.168.24.28:9042/api/products/01734',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:14:20.4748107+05:00',
      'Processing1BeginTime': '2025-01-28T12:18:16.8751141+05:00',
      'Processing2BeginTime': '2025-01-28T12:18:16.8751141+05:00',
      'Processing3BeginTime': '2025-01-28T12:33:12.7551857+05:00',
      'Processing4BeginTime': '2025-01-28T12:33:12.7551857+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:33:13.3045875+05:00',
      'ServeTime': '2025-01-28T12:33:14.2882186+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': '15c24320-ed56-4719-8789-6d6d2574ef6c',
    'Amount': 1.0,
    'ProductName': 'Burn 0,5л',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 4,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:14:57.2856594+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:14:57.3013369+05:00',
    'Processing1BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'Processing2BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'Processing3BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'Processing4BeginTime': '2025-01-28T12:33:12.7551857+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:33:13.3045875+05:00',
    'ServeTime': '2025-01-28T12:33:14.2882186+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0,5л',
      'KitchenName': '0,5л'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01857',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Burn',
      'AllowProductsCombining': False,
      'Scale': 'Напитки'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/21143155-23ca-4666-876b-6b61246910ec',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/15'
}, {
  'Id': 'c1228fa2-2d9e-422e-b17b-d592490b05f5',
  'Number': 14,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '738b88d9-3511-42d2-95b5-48126f1c8435',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:13:30.4416079+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:13:30.4416079+05:00',
    'Processing1BeginTime': '2025-01-28T12:18:19.2612135+05:00',
    'Processing2BeginTime': '2025-01-28T12:18:19.2612135+05:00',
    'Processing3BeginTime': '2025-01-28T12:31:58.4009212+05:00',
    'Processing4BeginTime': '2025-01-28T12:33:05.187197+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:33:05.826928+05:00',
    'ServeTime': '2025-01-28T12:33:06.5106934+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '8068fde0-5625-41fc-beee-74d3c714a5f9',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Без красного',
      'Product': 'http://192.168.24.28:9042/api/products/01733',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:13:30.4416079+05:00',
      'Processing1BeginTime': '2025-01-28T12:18:19.2612135+05:00',
      'Processing2BeginTime': '2025-01-28T12:18:19.2612135+05:00',
      'Processing3BeginTime': '2025-01-28T12:31:58.4009212+05:00',
      'Processing4BeginTime': '2025-01-28T12:33:05.187197+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:33:05.826928+05:00',
      'ServeTime': '2025-01-28T12:33:06.5106934+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }, {
      'Id': 'c2db232b-0fbd-40b5-a5da-5cc34066309c',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Без лука',
      'Product': 'http://192.168.24.28:9042/api/products/01734',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:13:30.4416079+05:00',
      'Processing1BeginTime': '2025-01-28T12:18:19.2612135+05:00',
      'Processing2BeginTime': '2025-01-28T12:18:19.2612135+05:00',
      'Processing3BeginTime': '2025-01-28T12:31:58.4009212+05:00',
      'Processing4BeginTime': '2025-01-28T12:33:05.187197+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:33:05.826928+05:00',
      'ServeTime': '2025-01-28T12:33:06.5106934+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }, {
      'Id': 'b6bd1567-ef74-4c4b-b19a-2b975d3eb091',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Картофель фри.',
      'Product': 'http://192.168.24.28:9042/api/products/01743',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:13:30.4416079+05:00',
      'Processing1BeginTime': '2025-01-28T12:18:19.2612135+05:00',
      'Processing2BeginTime': '2025-01-28T12:18:19.2612135+05:00',
      'Processing3BeginTime': '2025-01-28T12:31:58.4009212+05:00',
      'Processing4BeginTime': '2025-01-28T12:33:05.187197+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:33:05.826928+05:00',
      'ServeTime': '2025-01-28T12:33:06.5106934+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/70b61e13-2dee-4aa1-96a6-9656a11b499c',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/14'
}, {
  'Id': '5557c609-dbfd-49b5-8788-f9b10ccd4bf6',
  'Number': 13,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'cf53cf7d-b095-4b7e-bf74-f6f60aa13357',
    'Amount': 1.0,
    'ProductName': 'Шаурма с индейкой мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:04:27.8123635+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:04:27.831275+05:00',
    'Processing1BeginTime': '2025-01-28T12:12:46.4550382+05:00',
    'Processing2BeginTime': '2025-01-28T12:12:46.4550382+05:00',
    'Processing3BeginTime': '2025-01-28T12:12:46.9080573+05:00',
    'Processing4BeginTime': '2025-01-28T12:12:49.2477599+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:12:53.3782825+05:00',
    'ServeTime': '2025-01-28T12:23:31.8557141+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '914e6ee9-6320-40af-850d-c9942dc4f58c',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Посильнее прожарить',
      'Product': 'http://192.168.24.28:9042/api/products/01748',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:04:27.831275+05:00',
      'Processing1BeginTime': '2025-01-28T12:12:46.4550382+05:00',
      'Processing2BeginTime': '2025-01-28T12:12:46.4550382+05:00',
      'Processing3BeginTime': '2025-01-28T12:12:46.9080573+05:00',
      'Processing4BeginTime': '2025-01-28T12:12:49.2477599+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:12:53.3782825+05:00',
      'ServeTime': '2025-01-28T12:23:31.8557141+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00824',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': 'dfb98d8c-7500-49f3-a7c3-291ec777bf70',
    'Amount': 1.0,
    'ProductName': 'Чай 0.2',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:23:31.7929697+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:23:31.8066289+05:00',
    'Processing1BeginTime': '2025-01-28T12:25:18.2969543+05:00',
    'Processing2BeginTime': '2025-01-28T12:25:18.2969543+05:00',
    'Processing3BeginTime': '2025-01-28T12:25:18.7583686+05:00',
    'Processing4BeginTime': '2025-01-28T12:25:18.7583686+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:25:20.2859712+05:00',
    'ServeTime': '2025-01-28T12:25:21.5822012+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0.2',
      'KitchenName': '0.2'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00922',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Чай',
      'AllowProductsCombining': False,
      'Scale': 'Размер_Чай'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/974b7e8c-45ac-4309-95a6-4a5f8d3312a1',
  'OrderType': 'Доставка самовывоз',
  'OrderServiceType': 2,
  'IsDeliverySelfService': True,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/13'
}, {
  'Id': '19b1d686-ff2c-4ecc-81e5-da49ae08ba6d',
  'Number': 12,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '12c461aa-2514-4479-9712-b32f06a7b7bc',
    'Amount': 1.0,
    'ProductName': 'Шаурма с индейкой мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': True,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:04:19.1028536+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:04:19.127278+05:00',
    'Processing1BeginTime': None,
    'Processing2BeginTime': None,
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 0,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '526675e9-10c8-4257-813f-91ac42422fbe',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Посильнее прожарить',
      'Product': 'http://192.168.24.28:9042/api/products/01748',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': True,
      'EstimatedCookingBeginTime': '2025-01-28T12:04:19.127278+05:00',
      'Processing1BeginTime': None,
      'Processing2BeginTime': None,
      'Processing3BeginTime': None,
      'Processing4BeginTime': None,
      'ProcessingCompleteTime': None,
      'ServeTime': None,
      'ProcessingStatus': 0,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00824',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': '2852f3b6-32bf-4ecf-9e80-a8b5af481541',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица большая',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:08:19.0439836+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:08:19.0596095+05:00',
    'Processing1BeginTime': '2025-01-28T12:16:54.8006038+05:00',
    'Processing2BeginTime': '2025-01-28T12:16:54.8006038+05:00',
    'Processing3BeginTime': '2025-01-28T12:16:55.2725949+05:00',
    'Processing4BeginTime': '2025-01-28T12:16:55.8506199+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:16:56.6785518+05:00',
    'ServeTime': '2025-01-28T12:25:11.9283672+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'большая',
      'KitchenName': 'большая'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/fcfdc969-22a7-4d98-a871-c7a1a6e74b73',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/12'
}, {
  'Id': '90b3405e-1c54-4b97-a1e8-a9670c6dcb02',
  'Number': 11,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '9084c14f-1970-4f59-ba49-d10708a80445',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:03:21.6348802+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:03:21.6504895+05:00',
    'Processing1BeginTime': '2025-01-28T12:11:27.3401969+05:00',
    'Processing2BeginTime': '2025-01-28T12:11:27.3401969+05:00',
    'Processing3BeginTime': '2025-01-28T12:11:27.3401969+05:00',
    'Processing4BeginTime': '2025-01-28T12:11:27.3401969+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:11:57.1676714+05:00',
    'ServeTime': '2025-01-28T12:12:17.0812434+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/d906c653-c0ef-48c2-a7f2-4a09171b8333',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/11'
}, {
  'Id': '3b80638c-f906-4a64-a1ae-1faf80e5cd13',
  'Number': 10,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '73669df5-e355-4c94-9dd9-ad7166f6e0cf',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:02:58.3764552+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:02:58.3920791+05:00',
    'Processing1BeginTime': '2025-01-28T12:11:24.0642268+05:00',
    'Processing2BeginTime': '2025-01-28T12:11:24.0642268+05:00',
    'Processing3BeginTime': '2025-01-28T12:11:24.0642268+05:00',
    'Processing4BeginTime': '2025-01-28T12:11:24.0642268+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:11:43.2987328+05:00',
    'ServeTime': '2025-01-28T12:11:44.3205311+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/ad22837c-6183-4cd1-9a78-01d5b59f3cd1',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/10'
}, {
  'Id': '8da1289f-3177-4f5e-abed-f3c8e3c88040',
  'Number': 9,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '1857a2ae-a8c5-43ed-b500-f8e43c948c25',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:02:38.1419227+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:02:38.1575453+05:00',
    'Processing1BeginTime': '2025-01-28T12:11:21.6865189+05:00',
    'Processing2BeginTime': '2025-01-28T12:11:21.6865189+05:00',
    'Processing3BeginTime': '2025-01-28T12:11:21.6865189+05:00',
    'Processing4BeginTime': '2025-01-28T12:11:21.6865189+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:11:42.0688448+05:00',
    'ServeTime': '2025-01-28T12:11:42.7676188+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': 'ebd82b3b-407a-4032-8e0b-35d764c1f267',
    'Amount': 1.0,
    'ProductName': 'Морс в ассотрименте 0,3л',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:02:38.1419227+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:02:38.1575453+05:00',
    'Processing1BeginTime': '2025-01-28T12:11:42.0688448+05:00',
    'Processing2BeginTime': '2025-01-28T12:11:42.0688448+05:00',
    'Processing3BeginTime': '2025-01-28T12:11:42.0688448+05:00',
    'Processing4BeginTime': '2025-01-28T12:11:42.0688448+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:11:42.0688448+05:00',
    'ServeTime': '2025-01-28T12:11:42.7676188+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0,3л',
      'KitchenName': '0,3л'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '68c49482-4aa2-41d4-b5b2-50894855b7ee',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Клюква',
      'Product': 'http://192.168.24.28:9042/api/products/01711',
      'KitchenName': 'Выдача',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:02:38.1575453+05:00',
      'Processing1BeginTime': '2025-01-28T12:11:42.0688448+05:00',
      'Processing2BeginTime': '2025-01-28T12:11:42.0688448+05:00',
      'Processing3BeginTime': '2025-01-28T12:11:42.0688448+05:00',
      'Processing4BeginTime': '2025-01-28T12:11:42.0688448+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:11:42.0688448+05:00',
      'ServeTime': '2025-01-28T12:11:42.7676188+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00945',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Морс',
      'AllowProductsCombining': False,
      'Scale': 'Напитки'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/d0c2141c-34e8-4ca8-8d0c-b3cd6546be2d',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/9'
}, {
  'Id': 'fec38828-7c1e-40bd-87c0-f3ef3068eb56',
  'Number': 8,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '185328ad-4189-49ca-8289-2210cc7b676b',
    'Amount': 1.0,
    'ProductName': 'Комбо набор №1',
    'Product': None,
    'KitchenName': 'Шашлычник',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%A8%D0%B0%D1%88%D0%BB%D1%8B%D1%87%D0%BD%D0%B8%D0%BA',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:01:49.203277+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:01:49.2189001+05:00',
    'Processing1BeginTime': '2025-01-28T12:39:50.1613838+05:00',
    'Processing2BeginTime': '2025-01-28T12:39:50.1613838+05:00',
    'Processing3BeginTime': '2025-01-28T12:39:50.8197701+05:00',
    'Processing4BeginTime': '2025-01-28T12:39:50.8197701+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:39:51.4808961+05:00',
    'ServeTime': '2025-01-28T12:39:52.8878966+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:40:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01287',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Морс для комбо',
      'AllowProductsCombining': False,
      'Scale': None
    }
  }, {
    'Id': '1ce4910d-3415-42c1-8df1-d1c08b3b4462',
    'Amount': 1.0,
    'ProductName': 'Комбо набор №6',
    'Product': None,
    'KitchenName': 'Шашлычник',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%A8%D0%B0%D1%88%D0%BB%D1%8B%D1%87%D0%BD%D0%B8%D0%BA',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:01:49.203277+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:01:49.2189001+05:00',
    'Processing1BeginTime': '2025-01-28T12:39:50.1613838+05:00',
    'Processing2BeginTime': '2025-01-28T12:39:50.1613838+05:00',
    'Processing3BeginTime': '2025-01-28T12:39:50.8197701+05:00',
    'Processing4BeginTime': '2025-01-28T12:39:50.8197701+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:39:51.4808961+05:00',
    'ServeTime': '2025-01-28T12:39:52.8878966+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:40:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01292',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Комбо лимонад',
      'AllowProductsCombining': False,
      'Scale': None
    }
  }, {
    'Id': 'ec79fca5-0cb6-47f3-b533-8dce4cba4681',
    'Amount': 2.0,
    'ProductName': 'Соус Heinz 25мл',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:01:49.203277+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:01:49.2189001+05:00',
    'Processing1BeginTime': '2025-01-28T12:39:50.1613838+05:00',
    'Processing2BeginTime': '2025-01-28T12:39:50.1613838+05:00',
    'Processing3BeginTime': '2025-01-28T12:39:50.8197701+05:00',
    'Processing4BeginTime': '2025-01-28T12:39:50.8197701+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:39:51.4808961+05:00',
    'ServeTime': '2025-01-28T12:39:52.8878966+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [{
      'Id': 'a5db5d03-0d38-4799-b6c3-c3297a9035e5',
      'Amount': 2.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Сырный',
      'Product': 'http://192.168.24.28:9042/api/products/02157',
      'KitchenName': 'Выдача',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:01:49.2189001+05:00',
      'Processing1BeginTime': '2025-01-28T12:39:50.1613838+05:00',
      'Processing2BeginTime': '2025-01-28T12:39:50.1613838+05:00',
      'Processing3BeginTime': '2025-01-28T12:39:50.8197701+05:00',
      'Processing4BeginTime': '2025-01-28T12:39:50.8197701+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:39:51.4808961+05:00',
      'ServeTime': '2025-01-28T12:39:52.8878966+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00868',
      'Amount': 2.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'heinz',
      'AllowProductsCombining': False,
      'Scale': None
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/cdd36a72-4d82-45ac-876c-5307955aea2f',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/8'
}, {
  'Id': '319be8fd-b921-4f32-b5f1-b5650aa353ea',
  'Number': 6,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'd87bbf2a-12e0-47a0-b2e3-d23fe17bfacf',
    'Amount': 0.45,
    'ProductName': 'Корейка, 1кг',
    'Product': 'http://192.168.24.28:9042/api/products/00853',
    'KitchenName': 'Шашлычник',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%A8%D0%B0%D1%88%D0%BB%D1%8B%D1%87%D0%BD%D0%B8%D0%BA',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T11:40:17.5878399+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T11:40:17.6034597+05:00',
    'Processing1BeginTime': '2025-01-28T11:41:09.4411153+05:00',
    'Processing2BeginTime': '2025-01-28T11:41:09.4411153+05:00',
    'Processing3BeginTime': '2025-01-28T11:41:10.3159098+05:00',
    'Processing4BeginTime': '2025-01-28T11:41:10.3159098+05:00',
    'ProcessingCompleteTime': '2025-01-28T11:41:12.0610366+05:00',
    'ServeTime': '2025-01-28T11:41:13.115254+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:40:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [],
    'IsCompound': False,
    'PrimaryComponent': None,
    'SecondaryComponent': None,
    'Template': None
  }, {
    'Id': '7a4d5092-485c-4058-b323-cef9e45f2115',
    'Amount': 1.0,
    'ProductName': 'Соус белый 100г',
    'Product': 'http://192.168.24.28:9042/api/products/00875',
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T11:40:17.5878399+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T11:40:17.6034597+05:00',
    'Processing1BeginTime': '2025-01-28T11:41:09.4411153+05:00',
    'Processing2BeginTime': '2025-01-28T11:41:09.4411153+05:00',
    'Processing3BeginTime': '2025-01-28T11:41:10.3159098+05:00',
    'Processing4BeginTime': '2025-01-28T11:41:10.3159098+05:00',
    'ProcessingCompleteTime': '2025-01-28T11:41:12.0610366+05:00',
    'ServeTime': '2025-01-28T11:41:13.115254+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [],
    'IsCompound': False,
    'PrimaryComponent': None,
    'SecondaryComponent': None,
    'Template': None
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/21be82f2-3e44-4f88-9b3e-3c3c9a1fe7d7',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/6'
}, {
  'Id': '7d13a584-06d4-4e1f-9079-d485edcaf33f',
  'Number': 7,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'a63b7fc8-7419-47d0-8ed2-9352aee25855',
    'Amount': 2.0,
    'ProductName': 'Шаурма Курица сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T11:37:08.3593358+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T11:37:08.3781185+05:00',
    'Processing1BeginTime': '2025-01-28T11:41:31.9436036+05:00',
    'Processing2BeginTime': '2025-01-28T11:41:31.9436036+05:00',
    'Processing3BeginTime': '2025-01-28T11:45:13.8459952+05:00',
    'Processing4BeginTime': '2025-01-28T11:45:13.8459952+05:00',
    'ProcessingCompleteTime': '2025-01-28T11:45:15.782782+05:00',
    'ServeTime': '2025-01-28T11:58:32.5852459+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 2.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/80e59e45-0dcc-466d-b6ee-4a7ba01240c1',
  'OrderType': 'Доставка самовывоз',
  'OrderServiceType': 2,
  'IsDeliverySelfService': True,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/7'
}, {
  'Id': 'c0d9ea04-a20c-4239-9a0b-184c514a970c',
  'Number': 5,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'e502e841-60f6-4ae6-8829-34d9afd662b2',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T11:27:48.3851058+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T11:27:48.4007189+05:00',
    'Processing1BeginTime': '2025-01-28T11:30:01.4613329+05:00',
    'Processing2BeginTime': '2025-01-28T11:30:01.4613329+05:00',
    'Processing3BeginTime': '2025-01-28T11:33:45.4402835+05:00',
    'Processing4BeginTime': '2025-01-28T11:33:45.4402835+05:00',
    'ProcessingCompleteTime': '2025-01-28T11:33:57.0420275+05:00',
    'ServeTime': '2025-01-28T11:34:26.8798597+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': 'ce6a02a0-5120-4e95-afab-a6e951b43746',
    'Amount': 1.0,
    'ProductName': 'Чай 0.2',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T11:27:48.3851058+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T11:27:48.4007189+05:00',
    'Processing1BeginTime': '2025-01-28T11:33:57.0420275+05:00',
    'Processing2BeginTime': '2025-01-28T11:33:57.0420275+05:00',
    'Processing3BeginTime': '2025-01-28T11:33:57.0420275+05:00',
    'Processing4BeginTime': '2025-01-28T11:33:57.0420275+05:00',
    'ProcessingCompleteTime': '2025-01-28T11:33:57.0420275+05:00',
    'ServeTime': '2025-01-28T11:34:26.8798597+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0.2',
      'KitchenName': '0.2'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00922',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Чай',
      'AllowProductsCombining': False,
      'Scale': 'Размер_Чай'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/4af687fa-8fc7-4e1f-a0aa-690d50ecdddd',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/5'
}, {
  'Id': '45012615-88a1-4f1d-ae8f-fd78a0897bd5',
  'Number': 17,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '2e81d052-d21b-41ee-b56c-e17caf3ae1ad',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:15:47.7791311+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:15:47.791919+05:00',
    'Processing1BeginTime': '2025-01-28T12:18:12.953632+05:00',
    'Processing2BeginTime': '2025-01-28T12:18:12.953632+05:00',
    'Processing3BeginTime': '2025-01-28T12:25:08.656831+05:00',
    'Processing4BeginTime': '2025-01-28T12:25:09.4291757+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:25:10.5845408+05:00',
    'ServeTime': '2025-01-28T12:25:56.6678474+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': '8abf931e-dc3d-46be-a102-39beb1187952',
    'Amount': 1.0,
    'ProductName': 'Лимонад Добрый в/а пластик 0,5л',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:25:56.605364+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:25:56.6209892+05:00',
    'Processing1BeginTime': '2025-01-28T12:28:12.8870378+05:00',
    'Processing2BeginTime': '2025-01-28T12:28:12.8870378+05:00',
    'Processing3BeginTime': '2025-01-28T12:28:13.3827971+05:00',
    'Processing4BeginTime': '2025-01-28T12:28:13.3827971+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:28:13.7550066+05:00',
    'ServeTime': '2025-01-28T12:28:14.3952313+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0,5л',
      'KitchenName': '0,5л'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '42eac807-d98f-4945-a736-16450a1fbeab',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Кола',
      'Product': 'http://192.168.24.28:9042/api/products/01788',
      'KitchenName': 'Выдача',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T12:25:56.6209892+05:00',
      'Processing1BeginTime': '2025-01-28T12:28:12.8870378+05:00',
      'Processing2BeginTime': '2025-01-28T12:28:12.8870378+05:00',
      'Processing3BeginTime': '2025-01-28T12:28:13.3827971+05:00',
      'Processing4BeginTime': '2025-01-28T12:28:13.3827971+05:00',
      'ProcessingCompleteTime': '2025-01-28T12:28:13.7550066+05:00',
      'ServeTime': '2025-01-28T12:28:14.3952313+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01793',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Лимонад Добрый',
      'AllowProductsCombining': False,
      'Scale': 'Напитки'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/c700127d-c2cd-4075-a03d-1f0004d3f1c5',
  'OrderType': 'Доставка самовывоз',
  'OrderServiceType': 2,
  'IsDeliverySelfService': True,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/17'
}, {
  'Id': 'cdc4e332-dbf3-4fe8-ac97-5077f421832c',
  'Number': 3,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '4082afad-b312-4895-8b76-fdf625616f00',
    'Amount': 1.0,
    'ProductName': 'Шаурма Свинина сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T11:09:11.9833026+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T11:09:11.9945501+05:00',
    'Processing1BeginTime': '2025-01-28T11:14:13.9687601+05:00',
    'Processing2BeginTime': '2025-01-28T11:14:13.9687601+05:00',
    'Processing3BeginTime': '2025-01-28T11:20:01.870412+05:00',
    'Processing4BeginTime': '2025-01-28T11:20:02.0105821+05:00',
    'ProcessingCompleteTime': '2025-01-28T11:20:02.4386477+05:00',
    'ServeTime': '2025-01-28T11:20:02.625043+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00818',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/691cb457-cb4c-4c63-938d-b77e7d1c765a',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/3'
}, {
  'Id': 'bf8ef8e6-c9d5-4f73-af26-a99e02c1745a',
  'Number': 1,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'b2ab1e11-1927-40ec-9399-cc22b1645388',
    'Amount': 1.0,
    'ProductName': 'Шаурма Свинина большая',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T11:08:49.0167801+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T11:08:49.0423254+05:00',
    'Processing1BeginTime': '2025-01-28T11:14:11.9984011+05:00',
    'Processing2BeginTime': '2025-01-28T11:14:11.9984011+05:00',
    'Processing3BeginTime': '2025-01-28T11:19:13.5445146+05:00',
    'Processing4BeginTime': '2025-01-28T11:19:13.9564643+05:00',
    'ProcessingCompleteTime': '2025-01-28T11:19:14.3564939+05:00',
    'ServeTime': '2025-01-28T11:19:14.7767303+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'большая',
      'KitchenName': 'большая'
    },
    'Comment': None,
    'Modifiers': [{
      'Id': '67cce80d-6e44-4dcf-ac2f-02d6a11dbd68',
      'Amount': 1.0,
      'AmountIndependentOfParentAmount': False,
      'ProductName': 'Сырный лаваш',
      'Product': 'http://192.168.24.28:9042/api/products/02127',
      'KitchenName': 'Экран повара 1',
      'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
      'Deleted': False,
      'EstimatedCookingBeginTime': '2025-01-28T11:08:49.0423254+05:00',
      'Processing1BeginTime': '2025-01-28T11:14:11.9984011+05:00',
      'Processing2BeginTime': '2025-01-28T11:14:11.9984011+05:00',
      'Processing3BeginTime': '2025-01-28T11:19:13.5445146+05:00',
      'Processing4BeginTime': '2025-01-28T11:19:13.9564643+05:00',
      'ProcessingCompleteTime': '2025-01-28T11:19:14.3564939+05:00',
      'ServeTime': '2025-01-28T11:19:14.7767303+05:00',
      'ProcessingStatus': 6,
      'CookingTime': None,
      'IsSeparate': False
    }],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00818',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/1ecc8c2c-62ab-480b-b03c-d3ba4bfa2efe',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/1'
}, {
  'Id': '04aa7d21-0d0d-4e06-acc9-2a544f80bd5e',
  'Number': 2,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'a2acd108-30ee-4997-b13b-b9af13253ab1',
    'Amount': 2.0,
    'ProductName': 'Шаурма Свинина сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T11:02:36.9088902+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T11:02:36.940141+05:00',
    'Processing1BeginTime': '2025-01-28T11:14:09.8080201+05:00',
    'Processing2BeginTime': '2025-01-28T11:14:09.8080201+05:00',
    'Processing3BeginTime': '2025-01-28T11:19:15.4565824+05:00',
    'Processing4BeginTime': '2025-01-28T11:20:01.4060346+05:00',
    'ProcessingCompleteTime': '2025-01-28T11:20:01.5705199+05:00',
    'ServeTime': '2025-01-28T11:20:01.7226162+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00818',
      'Amount': 2.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/7e55c365-0755-4468-847f-cd082c5c9f7a',
  'OrderType': 'Доставка самовывоз',
  'OrderServiceType': 2,
  'IsDeliverySelfService': True,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/2'
}, {
  'Id': '9ce1b13b-9306-45cf-9938-05013a3185a2',
  'Number': 242,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'c3cac61a-2c42-4a94-95e7-47fbd07fc544',
    'Amount': 1.0,
    'ProductName': 'Шаурма Свинина мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': True,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2024-12-21T21:02:49.133+05:00',
    'EstimatedCookingBeginTime': '2024-12-21T21:02:49.148+05:00',
    'Processing1BeginTime': '2024-12-21T21:04:28.763+05:00',
    'Processing2BeginTime': '2024-12-21T21:04:28.763+05:00',
    'Processing3BeginTime': '2024-12-21T21:04:28.763+05:00',
    'Processing4BeginTime': '2024-12-21T21:09:14.575+05:00',
    'ProcessingCompleteTime': '2024-12-21T21:10:02.481+05:00',
    'ServeTime': '2024-12-21T22:26:53.932+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00818',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/10143464-8377-4a68-bf38-10268c900c76',
  'OrderType': 'Доставка самовывоз',
  'OrderServiceType': 2,
  'IsDeliverySelfService': True,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/242'
}, {
  'Id': '9a4004dd-d1a5-4672-bd7c-ea6f9fb8fc02',
  'Number': 24,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '52a53654-3dec-46db-a4c4-769cee824725',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:37:13.162805+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:37:13.178635+05:00',
    'Processing1BeginTime': '2025-01-28T12:39:44.9588274+05:00',
    'Processing2BeginTime': '2025-01-28T12:39:44.9588274+05:00',
    'Processing3BeginTime': '2025-01-28T12:42:45.4545676+05:00',
    'Processing4BeginTime': '2025-01-28T12:42:45.4545676+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:42:46.0404812+05:00',
    'ServeTime': '2025-01-28T12:43:15.2081768+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': '9e2f4be0-97e1-4582-afc9-611655256f4a',
    'Amount': 1.0,
    'ProductName': 'Чай 0.3',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:37:13.162805+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:37:13.178635+05:00',
    'Processing1BeginTime': '2025-01-28T12:42:45.4545676+05:00',
    'Processing2BeginTime': '2025-01-28T12:42:45.4545676+05:00',
    'Processing3BeginTime': '2025-01-28T12:42:45.4545676+05:00',
    'Processing4BeginTime': '2025-01-28T12:42:45.4545676+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:42:46.0404812+05:00',
    'ServeTime': '2025-01-28T12:43:15.2081768+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0.3',
      'KitchenName': '0.3'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00922',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Чай',
      'AllowProductsCombining': False,
      'Scale': 'Размер_Чай'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/07339e20-e94e-4594-945f-12164c270095',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/24'
}, {
  'Id': '5689d911-318a-4e71-b84f-46452756a40e',
  'Number': 25,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '524989bd-8c38-4f0c-8ef5-8bda11139b01',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица мал',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:38:07.1876879+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:38:07.2014815+05:00',
    'Processing1BeginTime': '2025-01-28T12:39:46.8584943+05:00',
    'Processing2BeginTime': '2025-01-28T12:39:46.8584943+05:00',
    'Processing3BeginTime': '2025-01-28T12:45:17.0691391+05:00',
    'Processing4BeginTime': '2025-01-28T12:45:17.0691391+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:46:51.3355689+05:00',
    'ServeTime': '2025-01-28T12:46:51.9140586+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'мал',
      'KitchenName': 'мал'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': '37f7aba4-8738-41b7-8220-f25f831b3337',
    'Amount': 1.0,
    'ProductName': 'Американо 0.2',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:38:07.1876879+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:38:07.2014815+05:00',
    'Processing1BeginTime': '2025-01-28T12:46:51.3355689+05:00',
    'Processing2BeginTime': '2025-01-28T12:46:51.3355689+05:00',
    'Processing3BeginTime': '2025-01-28T12:46:51.3355689+05:00',
    'Processing4BeginTime': '2025-01-28T12:46:51.3355689+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:46:51.3355689+05:00',
    'ServeTime': '2025-01-28T12:46:51.9140586+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0.2',
      'KitchenName': '0.2'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01295',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Кофе',
      'AllowProductsCombining': False,
      'Scale': 'Кофе'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/220f0a89-794e-4b98-a6dc-128d17782954',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/25'
}, {
  'Id': '265773e0-ba8a-4de4-a94a-1bee9f4d9ab7',
  'Number': 26,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'c1d5b48d-cfb7-4f74-9e35-c68a4390d4a3',
    'Amount': 1.0,
    'ProductName': 'Комбо набор №1',
    'Product': None,
    'KitchenName': 'Шашлычник',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%A8%D0%B0%D1%88%D0%BB%D1%8B%D1%87%D0%BD%D0%B8%D0%BA',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:44:50.205827+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:44:50.2216321+05:00',
    'Processing1BeginTime': '2025-01-28T12:46:53.2163889+05:00',
    'Processing2BeginTime': '2025-01-28T12:46:53.2163889+05:00',
    'Processing3BeginTime': '2025-01-28T12:46:53.788526+05:00',
    'Processing4BeginTime': '2025-01-28T12:46:53.788526+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:46:54.5003767+05:00',
    'ServeTime': '2025-01-28T12:46:54.8879406+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:40:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01287',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Морс для комбо',
      'AllowProductsCombining': False,
      'Scale': None
    }
  }, {
    'Id': 'b37de220-211e-4f83-b06e-60c3a61d5761',
    'Amount': 1.0,
    'ProductName': 'Соус белый 100г',
    'Product': 'http://192.168.24.28:9042/api/products/00875',
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:44:50.205827+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:44:50.2216321+05:00',
    'Processing1BeginTime': '2025-01-28T12:46:53.2163889+05:00',
    'Processing2BeginTime': '2025-01-28T12:46:53.2163889+05:00',
    'Processing3BeginTime': '2025-01-28T12:46:53.788526+05:00',
    'Processing4BeginTime': '2025-01-28T12:46:53.788526+05:00',
    'ProcessingCompleteTime': '2025-01-28T12:46:54.5003767+05:00',
    'ServeTime': '2025-01-28T12:46:54.8879406+05:00',
    'ProcessingStatus': 6,
    'CookingTime': '00:10:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [],
    'IsCompound': False,
    'PrimaryComponent': None,
    'SecondaryComponent': None,
    'Template': None
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/ef7d0aa1-1da7-4a9f-8c1d-5611b729ea37',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/26'
}, {
  'Id': '659bef30-eba0-42cd-8cdb-bdc174fd76ca',
  'Number': 27,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '1036d5d2-51cc-43aa-ad44-ffcf6861e3f1',
    'Amount': 1.0,
    'ProductName': 'Комбо набор №3',
    'Product': None,
    'KitchenName': 'Шашлычник',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%A8%D0%B0%D1%88%D0%BB%D1%8B%D1%87%D0%BD%D0%B8%D0%BA',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:49:19.2715873+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:49:19.2827789+05:00',
    'Processing1BeginTime': None,
    'Processing2BeginTime': None,
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 0,
    'CookingTime': '00:40:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/01289',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Морс для комбо',
      'AllowProductsCombining': False,
      'Scale': None
    }
  }, {
    'Id': '3a44fe06-72f6-458b-9ceb-b6326d5a4a4c',
    'Amount': 1.0,
    'ProductName': 'Соус белый 100г',
    'Product': 'http://192.168.24.28:9042/api/products/00875',
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:49:19.2715873+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:49:19.2827789+05:00',
    'Processing1BeginTime': None,
    'Processing2BeginTime': None,
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 0,
    'CookingTime': '00:10:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [],
    'IsCompound': False,
    'PrimaryComponent': None,
    'SecondaryComponent': None,
    'Template': None
  }, {
    'Id': 'a32eee28-c92f-42a4-ba2a-6a6dcc88925e',
    'Amount': 1.0,
    'ProductName': 'Лаваш',
    'Product': 'http://192.168.24.28:9042/api/products/00891',
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:49:19.2715873+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:49:19.2827789+05:00',
    'Processing1BeginTime': None,
    'Processing2BeginTime': None,
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 0,
    'CookingTime': '00:10:00',
    'Size': None,
    'Comment': None,
    'Modifiers': [],
    'IsCompound': False,
    'PrimaryComponent': None,
    'SecondaryComponent': None,
    'Template': None
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/2c7a313d-a9cd-4730-b30c-a99f8b8579ad',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/27'
}, {
  'Id': '7ea1822b-4004-4f98-8ed8-3a632f584ba9',
  'Number': 28,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'b97d0652-0a58-4d02-b0a4-2dd19561aeb7',
    'Amount': 1.0,
    'ProductName': 'Шаурма Свинина большая',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:54:14.0428132+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:54:14.0585971+05:00',
    'Processing1BeginTime': '2025-01-28T12:57:07.7243037+05:00',
    'Processing2BeginTime': '2025-01-28T12:57:07.7243037+05:00',
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 2,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'большая',
      'KitchenName': 'большая'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00818',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }, {
    'Id': 'f0b1bb90-8ecb-4b05-b6ca-d14d6de7a6a4',
    'Amount': 1.0,
    'ProductName': 'Чай 0.3',
    'Product': None,
    'KitchenName': 'Выдача',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%92%D1%8B%D0%B4%D0%B0%D1%87%D0%B0',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 2,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:54:14.0428132+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:54:14.0585971+05:00',
    'Processing1BeginTime': None,
    'Processing2BeginTime': None,
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 0,
    'CookingTime': '00:10:00',
    'Size': {
      'Name': '0.3',
      'KitchenName': '0.3'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00922',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Чай',
      'AllowProductsCombining': False,
      'Scale': 'Размер_Чай'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/9e134743-1195-42aa-83e1-c266f2b64940',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/28'
}, {
  'Id': 'c2e73524-3847-4eef-ab77-e822a833375e',
  'Number': 30,
  'WaiterName': None,
  'TableNum': 1,
  'Waiter': None,
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': 'da32a70d-2a34-4bed-bc09-a02fbf3d6fb6',
    'Amount': 1.0,
    'ProductName': 'Шаурма Курица сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:55:29.9098758+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:55:29.9255343+05:00',
    'Processing1BeginTime': '2025-01-28T12:57:09.7879681+05:00',
    'Processing2BeginTime': '2025-01-28T12:57:09.7879681+05:00',
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 2,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00827',
      'Amount': 1.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/813f0721-2825-4978-b294-cdb56718f64a',
  'OrderType': 'Доставка самовывоз',
  'OrderServiceType': 2,
  'IsDeliverySelfService': True,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/30'
}, {
  'Id': '1b0b5ca6-b881-4492-9a8e-1a46584e6d94',
  'Number': 29,
  'WaiterName': 'Нуриджанян Лусине',
  'TableNum': 1,
  'Waiter': 'http://192.168.24.28:9042/api/users/%D0%9D%D1%83%D1%80%D0%B8%D0%B4%D0%B6%D0%B0%D0%BD%D1%8F%D0%BD%20%D0%9B%D1%83%D1%81%D0%B8%D0%BD%D0%B5',
  'Table': 'http://192.168.24.28:9042/api/tables/1',
  'Items': [{
    'Id': '8f9a1824-de23-41c1-9a45-65c331d97ba7',
    'Amount': 2.0,
    'ProductName': 'Шаурма Свинина сред',
    'Product': None,
    'KitchenName': 'Экран повара 1',
    'Kitchen': 'http://192.168.24.28:9042/api/sections/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%20%D0%BF%D0%BE%D0%B2%D0%B0%D1%80%D0%B0%201',
    'Deleted': False,
    'Course': 1,
    'ServeGroupNumber': 1,
    'IsCookingStarted': True,
    'PrintTime': '2025-01-28T12:57:30.1565331+05:00',
    'EstimatedCookingBeginTime': '2025-01-28T12:57:30.1716685+05:00',
    'Processing1BeginTime': None,
    'Processing2BeginTime': None,
    'Processing3BeginTime': None,
    'Processing4BeginTime': None,
    'ProcessingCompleteTime': None,
    'ServeTime': None,
    'ProcessingStatus': 0,
    'CookingTime': '00:15:00',
    'Size': {
      'Name': 'сред',
      'KitchenName': 'сред'
    },
    'Comment': None,
    'Modifiers': [],
    'IsCompound': True,
    'PrimaryComponent': {
      'Product': 'http://192.168.24.28:9042/api/products/00818',
      'Amount': 2.0,
      'Modifiers': []
    },
    'SecondaryComponent': None,
    'Template': {
      'Name': 'Для шаурмы',
      'AllowProductsCombining': False,
      'Scale': 'Размер шаурмы'
    }
  }],
  'BaseOrder': 'http://192.168.24.28:9042/api/orders/999b917e-81fb-4877-b009-bb7f9c65709f',
  'OrderType': None,
  'OrderServiceType': 0,
  'IsDeliverySelfService': False,
  'OriginName': None,
  'ExternalNumber': None,
  'Url': 'http://192.168.24.28:9042/api/kitchenorders/29'
}]

    return data


def pull_kitchenorders():
    iko = iikoSettings.get_active()
    current_mill = round(time.time() * 1000)
    # Log.add_new(str(current_mill) + ' ' + str(iko.last_getting), 'Iiko', title2='drop_token()')

    if current_mill - int(iko.last_getting) > 20000:
        iko.last_getting = current_mill
        iko.save()

        data = get_kitchenorders()
        # return data
        # Получаем текущую дату в формате YYYY-MM-DD
        current_date = datetime.now().date()


        try:

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




