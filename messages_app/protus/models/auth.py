from django.db import models
from django.db.models import BooleanField, DateTimeField, CharField, ForeignKey, IntegerField


class ProtusAccessToken(models.Model):
    user_uuid = CharField(max_length=50, verbose_name='PROTUS uuid')
    token = CharField(max_length=300, verbose_name='PROTUS Access')
    expires_at = DateTimeField(verbose_name='Годен до')
    scope = CharField(max_length=100, verbose_name='Scope')

    class Meta:
        verbose_name = 'AccessToken'
        verbose_name_plural = 'AccessTokens'


class ProtusRefreshToken(models.Model):
    user_uuid = CharField(max_length=50, verbose_name='PROTUS uuid')
    token = CharField(max_length=300, verbose_name='PROTUS Refresh')
    access_token = ForeignKey(ProtusAccessToken, on_delete=models.CASCADE, verbose_name='Access', related_name='refresh')
    revoked = BooleanField(default=False)

    class Meta:
        verbose_name = 'RefreshToken'
        verbose_name_plural = 'RefreshTokens'


class OAuthLoginSession(models.Model):
    token_id = IntegerField(verbose_name='ID токена', null=True, blank=True)
    session_id = CharField(max_length=30, verbose_name='ID сессии')
    confirmation_id = CharField(max_length=20, verbose_name='ID подтверждения', null=True, blank=True)
    user_uuid = CharField(max_length=50, verbose_name='PROTUS uuid', null=True, blank=True)
    expire_date = DateTimeField(verbose_name='Действительна до')
    finalized_at = DateTimeField(verbose_name='Дата авторизации', null=True, blank=True)
    is_finalized = BooleanField(default=False)

    class Meta:
        verbose_name = 'Protus LoginSession'
        verbose_name_plural = 'Protus LoginSessions'
