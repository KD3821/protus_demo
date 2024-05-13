from django.urls import path

from protus.views import handle_webhook_request
from protus.urls.auth import urlpatterns as auth_urlpatterns


urlpatterns = [
    path('webhook', handle_webhook_request, name='webhook'),
] + auth_urlpatterns
