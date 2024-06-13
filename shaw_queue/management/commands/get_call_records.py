from shawarma.settings import ELASTIX_ACTION, ELASTIX_LOGIN, ELASTIX_SCRIPT, ELASTIX_SECRET, ELASTIX_SERVER
from django.core.management.base import BaseCommand, CommandError
from raven.contrib.django.raven_compat.models import client
from shaw_queue.models import CallData, Staff, Customer
from datetime import datetime
from requests.exceptions import HTTPError, TooManyRedirects, ConnectionError, Timeout
import requests
import logging
import time
import sys, traceback

logger_debug = logging.getLogger('debug_logger')


class Command(BaseCommand):
    help = 'Requests record data from Elastix'
    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)
    def handle(self, *args, **options):
        logger_debug.info(f'in get call records\n\n')

        # original_prefix = '/var/spool/asterisk/monitor'
        # substitute_prefix = '//192.168.20.25/rec/monitor'
        original_prefix = '/var/spool/asterisk/monitor'
        substitute_prefix = 'https://pbx.natruda.ru/monitor/'
        result = None
        try:
            self.stdout.write('Requesting records from {}'.format('https://' + ELASTIX_SERVER + '/' + ELASTIX_SCRIPT+'?'+'_login='+ ELASTIX_LOGIN+ '&_secret='+ ELASTIX_SECRET+
                                                                  '&_action='+ ELASTIX_ACTION))
            result = requests.get('https://' + ELASTIX_SERVER + '/' + ELASTIX_SCRIPT,
                                  params={'_login': ELASTIX_LOGIN, '_secret': ELASTIX_SECRET,
                                          '_action': ELASTIX_ACTION}, verify=False)
            result.raise_for_status()
            self.stdout.write(self.style.SUCCESS('Records requested successfully!'))
        except Timeout:
            self.stderr.write(self.style.ERROR('Превышено время ожидания соединения с Elastix при запросе записей разговоров!'))
            client.captureException()
        except TooManyRedirects:
            self.stderr.write(self.style.ERROR('Превышено количество перенаправлений при соединении с Elastix при запросе записей разговоров!'))
            client.captureException()
        except ConnectionError:
            self.stderr.write(self.style.ERROR('Возникла проблема соединения с Elastix при запросе записей разговоров!'))
            client.captureException()
        except HTTPError:
            self.stderr.write(self.style.ERROR('{}: Ошибка соединения с Elastix при запросе записей разговоров!'.format(result.status_code)))
            client.captureException()
        except:
            self.stderr.write(self.style.ERROR('Возникло необработанное исключение при запросе записей разговоров!'))
            client.captureException()

        if result is None:
            return
        if result.status_code == 200:
            records_data = None
            try:
                records_data = result.json()['data']
                print(records_data)
            except KeyError:
                self.stderr.write(self.style.ERROR('Нет data в ответе Elastix!'))
                client.captureException()

            for record in records_data[-300:]:
                if not record['recordingfile']:
                    continue

                try:
                    call = CallData.objects.get(ats_id=record['uniqueid'])
                except KeyError:
                    self.stderr.write(self.style.ERROR('Нет uniqueid в ответе Elastix!'))
                    client.captureException()
                except CallData.DoesNotExist:
                    recordingfile_list = record['recordingfile'].split('-')

                    if recordingfile_list[0] == 'external':
                        record_time = datetime.strptime(f'{recordingfile_list[3]} {recordingfile_list[4]}',
                                                        '%Y%m%d %H%M%S')

                        caller_id = recordingfile_list[2]
                        operator_id = int(recordingfile_list[1])
                        call_uid = recordingfile_list[5][:-4]

                        try:
                            customer = Customer.objects.get(phone_number="+{}".format(caller_id))
                            print("Choosing customer {}".format("+{}".format(caller_id)))
                        except Customer.DoesNotExist:
                            customer = Customer(phone_number="+{}".format(caller_id))
                            customer.save()
                        except Customer.MultipleObjectsReturned:
                            customer = Customer.objects.filter(phone_number="+{}".format(caller_id)).first()

                        try:
                            call_manager = Staff.objects.get(phone_number=operator_id)
                        except Staff.DoesNotExist:
                            continue
                        except Staff.MultipleObjectsReturned:
                            call_manager = Staff.objects.filter(phone_number=operator_id,
                                                                staff_category__title='Operator').first()

                        call = CallData(ats_id=call_uid, timepoint=record_time, customer=customer,
                                        call_manager=call_manager, accepted=True)
                    else:
                        continue

                try:
                    calldate = record['calldate'].split()
                    calldate = calldate[0].replace('-', '/')
                except KeyError:
                    self.stderr.write(self.style.ERROR('Нет calldate в ответе Elastix!'))
                    client.captureException()
                    continue

                try:
                    try:
                        call.duration = time.strftime("%H:%M:%S", time.gmtime(int(record['billsec'])))
                    except:
                        print(f'delivery_request ERROR: {traceback.format_exc()}')
                        pass

                    # record_url = substitute_prefix+(record['recordingfile'])[len(original_prefix):]
                    record_url = substitute_prefix + calldate + '/' + (record['recordingfile'])
                    print(record_url)
                    if call.record == "Record path not set" or call.record != record_url:
                        call.record = record_url
                        call.save()
                except KeyError:
                    self.stderr.write(self.style.ERROR('Нет recordingfile в ответе Elastix!'))
                    client.captureException()

        else:
            if result.status_code == 500:
                self.stderr.write(self.style.ERROR('500: Ошибка в обработке Elastix!'))
            else:
                if result.status_code == 400:
                    self.stderr.write(self.style.ERROR('400: Ошибка в запросе, отправленном в Elastix!'))
                else:
                    self.stderr.write(self.style.ERROR('{} в ответе 1С! Заказ удалён! Вы можете повторить попытку!'.format(result.status_code)))
