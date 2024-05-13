from rest_framework.decorators import api_view
from rest_framework import exceptions

from protus.handlers import WEBHOOK_HANDLERS
from protus.settings import api_settings


@api_view(['POST'])
def handle_webhook_request(request):
    data = request.data

    headers = request.headers

    if headers.get('Authorization') != api_settings.WEBHOOK_SECRET:
        raise exceptions.AuthenticationFailed(detail="Access denied")

    handler_type = headers.get('User-Type')

    handler = WEBHOOK_HANDLERS[handler_type]

    return handler(data)
