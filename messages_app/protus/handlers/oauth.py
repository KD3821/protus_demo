from rest_framework import status
from rest_framework.response import Response

from protus.utils.oauth import get_or_create_user_token, finalize_login_session


def provide_oauth_token(data):
    """
    Обработка веб-хука на создание аккаунта если нет, сохранение OAuth Access Token и финализацию сессии авторизации
    """
    access = data.get('access')
    email = data.get('email')
    username = data.get('username')
    finalized_at = data.get('finalized_at')
    session_id = data.get('session_id')
    confirmation_id = data.get('confirmation_id')
    session = finalize_login_session(session_id, finalized_at, confirmation_id)
    user_uuid, token_id = get_or_create_user_token(token=access, email=email, username=username)
    session.user_uuid = user_uuid
    session.token_id = token_id
    session.save(update_fields=['user_uuid', 'token_id'])
    return Response({'sid': session_id}, status=status.HTTP_201_CREATED)
