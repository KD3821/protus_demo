import os
import datetime
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
UI_HOST = os.getenv("UI_HOST")
UI_PORT = os.getenv("UI_PORT")
MQ_HOST = os.getenv("MQ_HOST")
CHANNELS_HOST = os.getenv("CHANNELS_HOST")
PROTUS_API_HOST = os.getenv("PROTUS_API_HOST")
PROTUS_API_PORT = os.getenv("PROTUS_API_PORT")
PROTUS_UI_HOST = os.getenv("PROTUS_UI_HOST")
PROTUS_UI_PORT = os.getenv("PROTUS_UI_PORT")


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',                     # noqa
    'rest_framework',
    'silk',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_celery_results',
    'django_celery_beat',
    'channels',

    'accounts',
    'service',
    'protus',                          # noqa
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Messages App API',
    'DESCRIPTION': 'Service for messaging customers',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR'
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'messages_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'messages_app.wsgi.application'

ASGI_APPLICATION = 'messages_app.asgi.application'

AUTH_USER_MODEL = 'accounts.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'protus.auth.authentication.CustomAuthentication',                         # noqa
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

PROTUS = {                                                         # noqa
    'PROTUS_HOST': f"http://{PROTUS_API_HOST}:{PROTUS_API_PORT}",  # noqa
    'PROTUS_UI': f"http://{PROTUS_UI_HOST}:{PROTUS_UI_PORT}",      # noqa
    'CLIENT_ID': os.getenv('CLIENT_ID'),
    'CLIENT_SECRET': os.getenv('CLIENT_SECRET'),
    'WEBHOOK_SECRET': os.getenv('WEBHOOK_SECRET'),
    'SUCCESS_LOGIN_URL': f"http://{UI_HOST}:{UI_PORT}/customers",  # noqa
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(minutes=3),
    'DEFAULT_TOKEN_SCOPE': 'check hold charge',
}

CELERY_BROKER_URL = f'amqp://{MQ_HOST}:5672'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND_DB = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_EXTENDED = True
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(f"{CHANNELS_HOST}", 6379)]
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': os.getenv('LOG_LEVEL'),
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.getenv('LOG_FILE'),
            'formatter': 'verbose'
        },
        'console': {
            'level': os.getenv('LOG_LEVEL'),
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'emails': {
            'handlers': ['file', 'console'],
            'level': os.getenv('LOG_LEVEL'),
            'propagate': True,
        },
        'users': {
            'handlers': ['file', 'console'],
            'level': os.getenv('LOG_LEVEL'),
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '-' * 8 + '\n[{levelname} | {asctime} | ({module})]:\n{message}\n' + '-' * 8 + '\n',
            'style': '{',
        },
    },
}
