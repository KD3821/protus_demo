import os
from datetime import datetime

import pytz
from rest_framework import status, exceptions
from jose import jwt, JWTError
from dotenv import load_dotenv

from django.contrib.auth import get_user_model
from django.utils import timezone

from protus.models import ProtusAccessToken, OAuthLoginSession
from protus.constants import JWT_ALGORITHM


load_dotenv()

JWT_SECRET = os.getenv('CLIENT_SECRET')

User = get_user_model()


def get_or_create_user_token(token, email, username):
    token_exception = exceptions.AuthenticationFailed(
        code=status.HTTP_403_FORBIDDEN,
        detail="Invalid token"
    )

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
    except JWTError:
        raise token_exception

    token_type = payload.get("token_type")

    if token_type != "access":
        raise token_exception

    user_uuid = payload.get("sub")

    try:
        user = User.objects.filter(uuid=user_uuid, email=email)[0:1].get()
    except User.DoesNotExist:
        user = User.objects.create_oauth_user(
            email=email, username=username, uuid=user_uuid
        )

    tz = timezone.get_current_timezone()
    expires_at = timezone.make_aware(datetime.fromtimestamp(payload.get('exp')), tz)

    token = ProtusAccessToken.objects.create(
        user_uuid=user.uuid,
        token=token,
        expires_at=expires_at,
        scope=payload.get('scope')
    )

    return user.uuid, token.pk


def finalize_login_session(session_id, finalized_at, confirmation_id):
    try:
        session = OAuthLoginSession.objects.filter(session_id=session_id, is_finalized=False)[0:1].get()

        fin_at = datetime.strptime(finalized_at, '%Y-%m-%d %H:%M:%S.%f')
        finalized_at = timezone.make_aware(fin_at, pytz.UTC)

        session.finalized_at = finalized_at
        session.confirmation_id = confirmation_id
        session.save()
        return session
    except OAuthLoginSession.DoesNotExist:
        raise exceptions.AuthenticationFailed(
            code=status.HTTP_403_FORBIDDEN,
            detail="Invalid session"
        )
