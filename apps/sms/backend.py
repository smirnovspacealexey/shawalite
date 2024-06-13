from .mango import send_sms as mango_send_sms
from .models import SMSHistory


def send_sms(phone, msg, data=None):
    if data:
        bad_result = []
        for i in data:
            sms = SMSHistory.objects.create(phone=i[0], text=i[1], result='в процессе')
            result = mango_send_sms(phone=i[0], msg=i[1], command_id=sms.pk)
            if not result[0]:
                bad_result.append(i)

            sms.success = result[0]
            sms.result = result[1]
            sms.save()

        if bad_result:
            return False, bad_result
        else:
            return True,

    sms = SMSHistory.objects.create(phone=phone, text=msg, result='в процессе')
    result = mango_send_sms(phone, msg, command_id=sms.pk)
    sms.success = result[0]
    sms.result = result[1]
    sms.save()
    return result[0], result[1]

