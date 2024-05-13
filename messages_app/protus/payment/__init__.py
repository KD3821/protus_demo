import urllib3
import uuid

import requests

from protus.utils import start_requests_session
from protus.constants import INTROSPECT_TOKEN_URL
from protus.settings import api_settings


def introspect_token(token):
    """
    Запрос на проверку валидности токена для OAuth_Verified пользователя
    """
    s = start_requests_session()
    try:
        response = s.post(
            url=f'{INTROSPECT_TOKEN_URL}',
            json={'access': token},
            headers={
                'Protus-Client': api_settings.CLIENT_ID,
                'Protus-Secret': api_settings.CLIENT_SECRET,
                'Idempotency-Key': str(uuid.uuid4())
            }
        )
    except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
        response = requests.models.Response()
        response.status_code = 500

    if response.status_code == 200:
        return response.json()

