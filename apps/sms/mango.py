import requests
import json
from hashlib import sha256
from .models import MangoSettings
from apps.logs.models import Log


def send_sms(phone, msg, command_id='', vpbx_api_key=None, vpbx_api_salt=None, from_extension=None):
    print('+', vpbx_api_key, vpbx_api_salt, from_extension)
    if not vpbx_api_key:
        vpbx_api_key, vpbx_api_salt, from_extension = MangoSettings.tokens()
        print('++', vpbx_api_key, vpbx_api_salt, from_extension)

    json_data = '{' + f'"command_id":"{command_id}","text":"{msg}","from_extension":"{from_extension}","to_number":"{phone}"' + '}'
    sign = sha256((vpbx_api_key + json_data + vpbx_api_salt).encode('utf-8')).hexdigest()
    print(vpbx_api_key + json_data + vpbx_api_salt)
    print(sign)

    data = {
        'vpbx_api_key': vpbx_api_key,
        'sign': sign,
        'json': json_data,
    }

    Log.add_new(f'Send to https://app.mango-office.ru/vpbx/commands/sms\n{str(data)}', 'SMS')

    res = requests.post('https://app.mango-office.ru/vpbx/commands/sms', data=data)
    response = json.loads(res.content.decode("utf-8"))

    Log.add_new(f'Result from mango\n{res.status_code}\n{str(response)}', 'SMS')
    print(res.status_code)
    print(response)
    if res.status_code == 200:
        return True, response['result']
    else:
        return False, (response['message'] + ' | code: ' + str(response['code'])) if response else res.status_code
