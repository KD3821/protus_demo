import urllib3
import uuid

import requests

from protus.utils import start_requests_session
from protus.constants import PROTUS_SESSION_URL
from protus.settings import api_settings


def request_login_session():
    """
    Запрос на получение сессии для авторизации - ответ содержит session_id, expire_date
    """
    s = start_requests_session()
    try:
        response = s.post(
            url=f'{PROTUS_SESSION_URL}',
            json={
                'client_id': api_settings.CLIENT_ID,
                'client_secret': api_settings.CLIENT_SECRET,
                'return_url': api_settings.SUCCESS_LOGIN_URL,
            },
            headers={
                'Protus-Client': api_settings.CLIENT_ID,      # ID & SECRET not required due to proxing GATEWAY > AUTH -
                'Protus-Secret': api_settings.CLIENT_SECRET,  # - just to keep same API for all requests...
                'Idempotency-Key': str(uuid.uuid4())          # also no caching for session in this version
            }
        )
    except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
        response = requests.models.Response()
        response.status_code = 500
    return response
