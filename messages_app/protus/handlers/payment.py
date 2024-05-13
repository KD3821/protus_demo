from datetime import datetime

import pytz
from rest_framework import status
from rest_framework.response import Response

from django.utils import timezone

from protus.models.payment import ProtusPayment


def finalize_payment(data):
    """
    Обработка веб-хука на финализацию оплаты услуги
    """
    invoice_number = data.get('invoice_number')
    reference_code = data.get('reference_code')
    finalized_at = data.get('finalized_at')
    payload = data.get('payload')

    timestamp = datetime.fromtimestamp(finalized_at)
    finalized_at = timezone.make_aware(timestamp, pytz.UTC)

    try:
        payment = ProtusPayment.objects.filter(invoice_number=invoice_number, status=ProtusPayment.INITIALIZED)[0:1].get()
        payment.status = ProtusPayment.SUCCEEDED
        payment.finalized_at = finalized_at
        payment.protus_note = f"PAID: {reference_code}"
        if payload:
            payment.payload = payload
        payment.save(update_fields=['status', 'finalized_at', 'protus_note', 'payload'])
        return Response({'code': reference_code}, status=status.HTTP_200_OK)

    except ProtusPayment.DoesNotExist:
        return Response({'detail': invoice_number}, status=status.HTTP_208_ALREADY_REPORTED)
