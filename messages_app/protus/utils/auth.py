from datetime import datetime

from rest_framework import status, exceptions
from jose import jwt, JWTError

from django.contrib.auth import get_user_model

from protus.models import ProtusAccessToken
from protus.auth.tokens import ProtusAuthTokenizer
from protus.constants import JWT_ALGORITHM
from protus.settings import api_settings


JWT_SECRET = api_settings.CLIENT_SECRET

User = get_user_model()


def verify_refresh_token(token):
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

    if token_type != "refresh":
        raise token_exception

    user_uuid = payload.get("sub")

    try:
        user = User.objects.filter(uuid=user_uuid)[0:1].get()
    except User.DoesNotExist:
        raise token_exception

    return user


def create_access_token(user):
    """
    Выпускаем новый Access Token (только для НЕ 'oauth_verified' пользователей)
    """
    now = datetime.utcnow()

    access_exp = now + api_settings.ACCESS_TOKEN_LIFETIME

    payload = {
        "token_type": "access",
        "iat": now,
        "nbf": now,
        "exp": access_exp,
        "sub": user.uuid,
        "scope": api_settings.DEFAULT_TOKEN_SCOPE
    }

    access = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    new_access_token = ProtusAccessToken.objects.create(
        user_uuid=user.uuid,
        token=access,
        expires_at=ProtusAuthTokenizer.provide_tz_support(access_exp),
        scope=api_settings.DEFAULT_TOKEN_SCOPE,
    )

    return new_access_token
