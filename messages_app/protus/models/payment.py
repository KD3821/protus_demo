from django.db import models
from django.db.models import CharField, DecimalField, DateTimeField, JSONField


class ProtusPayment(models.Model):
    INITIALIZED = 'initialized'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    PAYMENT_STATUSES = (
        (INITIALIZED, 'в обработке'),
        (SUCCEEDED, 'оплачен'),
        (FAILED, 'отклонен')
    )
    payment_uuid = CharField(max_length=50, verbose_name='ID платежа')
    user_uuid = CharField(max_length=50, verbose_name='PROTUS uuid')
    service_id = CharField(max_length=50, verbose_name='ID услуги')
    service_name = CharField(max_length=100, verbose_name='Название услуги')
    invoice_number = CharField(max_length=50, verbose_name='Номер инвойса')
    amount = DecimalField(max_digits=8, decimal_places=2, verbose_name='Сумма', null=True, blank=True)
    status = CharField(max_length=15, choices=PAYMENT_STATUSES, default=INITIALIZED, verbose_name='Статус платежа')
    payload = JSONField(verbose_name='Payload', null=True, blank=True)
    initialized_at = DateTimeField(verbose_name='Время инициализации')
    finalized_at = DateTimeField(verbose_name='Время оплаты', null=True, blank=True)
    protus_note = CharField(max_length=100, verbose_name='Пометка PROTUS', null=True, blank=True)

    class Meta:
        verbose_name = 'Protus Платеж'
        verbose_name_plural = 'Protus Платежи'
