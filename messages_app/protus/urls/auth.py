from django.urls import path

from protus.views.auth import oauth_login_session, oauth_confirm_session


# PROTUS urls
urlpatterns = [
    path('login-session', oauth_login_session, name='login_session'),
    path('confirm-session', oauth_confirm_session, name='confirm_session')
]
