from django.contrib import admin
from django.contrib.auth import get_user_model

from protus.models.payment import ProtusPayment
from protus.models.auth import (
    ProtusAccessToken,
    ProtusRefreshToken,
    OAuthLoginSession,
)

User = get_user_model()


@admin.register(ProtusAccessToken)
class ProtusAccessAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_uuid', 'expires_at', 'scope', 'token']
    list_filter = ['user_uuid']


@admin.register(ProtusRefreshToken)
class ProtusRefreshAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_uuid', 'access_token_id', 'revoked', 'token']
    list_filter = ['user_uuid']


@admin.register(OAuthLoginSession)
class OAuthLoginSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'expire_date', 'user_uuid', 'token_id', 'finalized_at', 'confirmation_id', 'is_finalized']
    list_filter = ['user_uuid', 'is_finalized']


@admin.register(ProtusPayment)
class ProtusPaymentAdmin(admin.ModelAdmin):
    list_display = ['email', 'service_id', 'amount', 'status', 'initialized_at', 'invoice_number', 'service_name',
                    'finalized_at', 'protus_note', 'payment_uuid']
    list_filter = ['status', 'service_name']

    def email(self, obj):
        user = User.objects.get(uuid=obj.user_uuid)
        return user.email
