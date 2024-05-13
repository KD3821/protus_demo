"""
Константы для запросов к PROTUS сервису
"""
from protus.settings import api_settings


# PROTUS CONSTANTS
JWT_ALGORITHM = 'HS256'  # Provided by PROTUS-CLI (for JWT tokens)
PROTUS_SESSION_URL = f'{api_settings.PROTUS_HOST}/oauth/session/'  # by PROTUS-CLI(fast_gate) request session (1st step)
OAUTH_SIGNIN_URL = f'{api_settings.PROTUS_UI}/oauth-signin'  # by PROTUS-CLI(protus_vue) oauth login page
CREATE_ACCOUNTING_URL = f'{api_settings.PROTUS_HOST}/billing/new-account/'  # by PROTUS-CLI(fast_gate) create accounting
INTROSPECT_TOKEN_URL = f'{api_settings.PROTUS_HOST}/oauth/introspect/'
CHARGE_REQUEST_URL = f'{api_settings.PROTUS_HOST}/billing/charge/'

# PROTUS ERROR DETAILS
ERROR_DETAILS = {
    403: 'Ошибка доступа. Проверьте правильность учетных данных'
}
