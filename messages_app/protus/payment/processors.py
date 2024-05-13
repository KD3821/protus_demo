import uuid
import urllib3
import threading
from datetime import datetime

import requests
import pytz

from django.utils import timezone

from protus.settings import api_settings
from protus.utils import start_requests_session
from protus.constants import CHARGE_REQUEST_URL
from protus.models.payment import ProtusPayment


class PaymentProcessor(threading.Thread):
    def __init__(self, user_uuid, service_id, payload=None):  # client's code may pass it's payment_id for own use
        if not isinstance(payload, (dict, type(None))):
            raise AttributeError('Param "payload" must be either "dict" or "None"')
        super().__init__()
        self.user_uuid = user_uuid
        self.service_id = service_id
        self.payload = payload
        self.idempotency_key = str(uuid.uuid4())

    def request_charge(self, idempotency_key):
        s = start_requests_session()
        try:
            response = s.post(
                url=f'{CHARGE_REQUEST_URL}',
                json={
                    'user_uuid': self.user_uuid,
                    'service_id': self.service_id,
                    'payload': self.payload,
                },
                headers={
                    'Protus-Client': api_settings.CLIENT_ID,    
                    'Protus-Secret': api_settings.CLIENT_SECRET,
                    'Idempotency-Key': idempotency_key,
                }
            )
        except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
            response = requests.models.Response()
            response.status_code = 500

        return response

    def run(self):
        res = self.request_charge(self.idempotency_key)
        now = timezone.now()
        if res.status_code == 200:
            charge_res = res.json()
            timestamp = datetime.fromtimestamp(charge_res.get('issued_at'))
            issued_at = timezone.make_aware(timestamp, pytz.UTC)
            ProtusPayment.objects.create(
                payment_uuid=self.idempotency_key,
                user_uuid=charge_res.get('user_uuid'),
                service_id=charge_res.get('service_id'),
                service_name=charge_res.get('service_name'),
                invoice_number=charge_res.get('invoice_number'),
                initialized_at=issued_at,
                amount=charge_res.get('amount')
            )
        else:
            ProtusPayment.objects.create(
                payment_uuid=self.idempotency_key,
                user_uuid=self.user_uuid,
                service_id=self.service_id,
                service_name="N/A",
                invoice_number="N/A",
                initialized_at=now,
                status=ProtusPayment.FAILED
            )
