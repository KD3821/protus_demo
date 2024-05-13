from django.urls import path

from .views import (
    RegisterView,
    LoginAPIView,
    LogoutAPIView,
)

from protus.views.auth import refresh_access_token


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh', refresh_access_token, name='token_refresh'),
]
