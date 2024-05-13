from rest_framework import status, serializers
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from django.contrib.auth.models import AnonymousUser
from django.utils.encoding import force_str
from django.utils import timezone

from protus.models.auth import ProtusAccessToken
from protus.payment import introspect_token


class ProtusValidationError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 'Ooops! Server error...'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else:
            self.detail = {'detail': force_str(self.default_detail)}


class ProtusChargePermission(BasePermission):
    charge_msg = 'Вы запретили взимать плату за услуги сервиса. Войдите с PROTUS, разрешив списание средств за услуги.'
    token_msg = 'Ошибка авторизации. Повторите вход'

    def has_permission(self, request, view):
        token_is_active = True
        if isinstance(request.user, AnonymousUser):
            raise ProtusValidationError(
                "Access Denied. Sign-In required.", "AccessToken", status_code=status.HTTP_403_FORBIDDEN
            )

        now = timezone.now()

        if request.user.oauth_verified:
            access_token = (
                ProtusAccessToken.objects
                .filter(user_uuid=request.user.uuid, expires_at__gt=now)
                .order_by('id').last()
            )

            if access_token is None:
                raise serializers.ValidationError({'detail': self.token_msg})

            scope_list = access_token.scope.split()

            if 'charge' not in scope_list:
                raise ProtusValidationError(self.charge_msg, "AccessToken", status_code=status.HTTP_426_UPGRADE_REQUIRED)

            data = introspect_token(access_token.token)  # todo also to use data.checked_at: int(unix-timestamp)

            if data.get('revoked') or 'charge' not in data.get('scope'):
                token_is_active = False

        return token_is_active
