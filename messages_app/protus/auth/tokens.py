import urllib3
import uuid
from datetime import datetime

import requests
import pytz
from jose import jwt
from rest_framework import exceptions

from django.utils import timezone

from protus.utils import start_requests_session
from protus.models import ProtusRefreshToken, ProtusAccessToken
from protus.constants import JWT_ALGORITHM, CREATE_ACCOUNTING_URL
from protus.settings import api_settings


JWT_SECRET = api_settings.CLIENT_SECRET
CLIENT_ID = api_settings.CLIENT_ID
CLIENT_SECRET = api_settings.CLIENT_SECRET


class ProtusAuthTokenizer:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def provide_tz_support(exp):
        expires_at = timezone.make_aware(exp, pytz.UTC)
        return expires_at

    def tokenize_user(self):
        if self.user.uuid is None:
            assign_protus_account_number(self.user)

        subject_id = self.user.uuid

        now = datetime.utcnow()

        access_exp = now + api_settings.ACCESS_TOKEN_LIFETIME

        payload = {
            "token_type": "access",
            "iat": now,
            "nbf": now,
            "exp": access_exp,
            "sub": subject_id,
            "scope": api_settings.DEFAULT_TOKEN_SCOPE
        }

        access = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        access_token = ProtusAccessToken.objects.create(
            user_uuid=self.user.uuid,
            token=access,
            expires_at=self.provide_tz_support(access_exp),
            scope=api_settings.DEFAULT_TOKEN_SCOPE
        )

        refresh_exp = now + api_settings.REFRESH_TOKEN_LIFETIME

        payload.update(
            {
                "token_type": "refresh",
                "exp": refresh_exp
            }
        )

        refresh = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        refresh_token = ProtusRefreshToken.objects.create(
            user_uuid=self.user.uuid,
            token=refresh,
            access_token=access_token,
            revoked=False
        )

        return refresh_token


def blacklist_token(refresh_token):
    try:
        token = ProtusRefreshToken.objects.filter(token=refresh_token, revoked=False)[0:1].get()
        token.revoked = True
        token.save()
    except ProtusRefreshToken.DoesNotExist:
        if refresh_token == "RefreshToken.NotProvided.OAuth":
            return
        raise exceptions.AuthenticationFailed(detail="bad_token")


def assign_protus_account_number(user):
    s = start_requests_session()
    try:
        response = s.post(
            url=f'{CREATE_ACCOUNTING_URL}',
            json={
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'email': user.email,
                'username': user.username
            },
            headers={
                'Protus-Client': CLIENT_ID,
                'Protus-Secret': CLIENT_SECRET,
                'Idempotency-Key': str(uuid.uuid4())
            }
        )
        if response.status_code == 200:
            account_number = response.json()
            user.uuid = account_number
            user.save(update_fields=['uuid'])

    except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
        response = requests.models.Response()
        response.status_code = 500
