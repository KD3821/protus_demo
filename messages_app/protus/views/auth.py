from datetime import datetime

import pytz
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.utils import timezone
from django.contrib.auth import get_user_model

from protus.models import ProtusRefreshToken, ProtusAccessToken, OAuthLoginSession
from protus.auth.session import request_login_session
from protus.utils.auth import (
    verify_refresh_token,
    create_access_token,
)
from protus.constants import OAUTH_SIGNIN_URL, ERROR_DETAILS


User = get_user_model()


@api_view(['POST'])
def refresh_access_token(request):
    """
    Обновление Access токена для Клиентского приложения
    """
    data = request.data
    refresh = data.get('refresh')
    try:
        refresh_token = ProtusRefreshToken.objects.filter(token=refresh, revoked=False)[0:1].get()
        user = verify_refresh_token(refresh_token.token)
        new_access = create_access_token(user)
        refresh_token.access_token = new_access
        refresh_token.save(update_fields=['access_token'])
        return Response(
            {'access': new_access.token}, status=status.HTTP_200_OK
        )
    except ProtusRefreshToken.DoesNotExist:
        return Response(
            {'detail': 'Необходимо повторно авторизоваться'}, status=status.HTTP_403_FORBIDDEN
        )


@api_view(['GET'])
def oauth_login_session(request):
    """
    Обработка запроса от Клиентского приложения на авторизацию через PROTUS (STEP 1)
    """
    res = request_login_session()
    if res.status_code == 200:
        now = datetime.utcnow()
        data = res.json()
        session_id = data.get('session_id')
        expire_date = data.get('expire_date')
        exp = datetime.strptime(expire_date, '%Y-%m-%dT%H:%M:%S.%f')
        if exp > now:
            aware_exp = timezone.make_aware(exp, pytz.UTC)
            OAuthLoginSession.objects.create(
                session_id=session_id,
                expire_date=aware_exp
            )
            return Response(
                {'login_url': f"{OAUTH_SIGNIN_URL}?sid={session_id}"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'detail': 'Время сессии истекло'}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {'detail': ERROR_DETAILS.get(res.status_code)}, res.status_code
        )


@api_view(['POST'])
def oauth_confirm_session(request):
    """
    Обработка результата сессии авторизации через PROTUS на странице успешной авторизации
    """
    data = request.data
    confirmation_id = data.get('confirmation_id')
    try:
        session = OAuthLoginSession.objects.filter(confirmation_id=confirmation_id, is_finalized=False)[0:1].get()
        user = User.objects.get(uuid=session.user_uuid)
        access_token = ProtusAccessToken.objects.get(id=session.token_id)

        session.is_finalized = True
        session.save()

        return Response(
            {
                'email': user.email,
                'username': user.username,
                'access': access_token.token,
                'refresh': 'RefreshToken.NotProvided.OAuth'
            },
            status=status.HTTP_200_OK
        )
    except OAuthLoginSession.DoesNotExist:
        return Response(
            {'detail': 'Ошибка авторизации'}, status=status.HTTP_403_FORBIDDEN
        )
