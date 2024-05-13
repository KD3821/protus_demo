from datetime import timedelta

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string


USER_SETTINGS = getattr(settings, "PROTUS", None)

DEFAULTS = {
    "PROTUS_HOST": "Please, set url for PROTUS API HOST",
    "PROTUS_UI": "Please, set url for PROTUS UI/WIDGET",
    "CLIENT_ID": "Please, set your client_id (check your dashboard at PROTUS-SERVICE)",
    "CLIENT_SECRET": "Please, set your client_secret (check your dashboard at PROTUS-SERVICE)",
    "WEBHOOK_SECRET": "Please, set your webhook_secret_key (check your dashboard at PROTUS-SERVICE)",
    "SUCCESS_LOGIN_URL": "Please, set your success_login_url for OAuth verified users",
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=10),
    "DEFAULT_TOKEN_SCOPE": "check hold charge",
}

REMOVED_SETTINGS = [
    "REVOKE_OAUTH_REFRESH_TOKEN_ON_LOGOUT",  # for example
]


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = f"Could not import '{val}' for API setting '{setting_name}'. {e.__class__.__name__}: {e}."
        raise ImportError(msg)


class APISettings:
    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'PROTUS', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid API setting: {attr}")

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        DOCS = "https://www.protus.org/docs/protus-django-settings/"
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    f"The '{setting}' setting has been removed. Please refer to '{DOCS}' for available settings."
                )
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


api_settings = APISettings(USER_SETTINGS, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'PROTUS':
        api_settings.reload()


setting_changed.connect(reload_api_settings)
