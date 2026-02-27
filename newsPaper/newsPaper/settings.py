from pathlib import Path
import os
from dotenv import load_dotenv
from django.utils.log import DEFAULT_LOGGING

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# Секретный ключ из .env
SECRET_KEY = os.getenv('SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-_k555bfu+28+@07h8auei@8q@6p(zv%qepik28rgtp$r123$h8"

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

LOGIN_URL = '/accounts/login/' 
LOGIN_REDIRECT_URL = '/news/' 
LOGOUT_REDIRECT_URL = '/news/' 

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',

    "django.contrib.flatpages",
    "news",
    "accounts",
    'django_filters',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = "newsPaper.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "newsPaper.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

DEBUG = False
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'console_debug': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
        'console_warning': {
            'format': '{asctime} {levelname} {pathname} {message}',
            'style': '{',
        },
        'console_error': {
            'format': '{asctime} {levelname} {pathname} {message}\n{exc_info}',
            'style': '{',
        },
        'general_file': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'errors_file': {
            'format': '{asctime} {levelname} {message} {pathname}\n{exc_info}',
            'style': '{',
        },
        'security_file': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'mail': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{',
        },
    },
    
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_debug',
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning',
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_error',
        },
        'general_file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'general.log'),
            'formatter': 'general_file',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'errors.log'),
            'formatter': 'errors_file',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
        'security_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'security.log'),
            'formatter': 'security_file',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail',
            'include_html': True,
        },
    },
    
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_error', 'general_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        
        'django.request': {
            'handlers': ['errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        
        'django.security': {
            'handlers': ['security_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your-email@gmail.com')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your-app-password')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'News Portal <noreply@newsportal.com>')
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
    
    ADMINS = [
        ('Admin','swooplida@gmail.com'),
    ]
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

LOGIN_REDIRECT_URL = '/news/'
LOGOUT_REDIRECT_URL = '/news/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account',
        },
        'VERIFIED_EMAIL': True,
        'EMAIL_AUTHENTICATION': True,
    },
    'yandex': {
        'APP': {
            'client_id': os.getenv('YANDEX_CLIENT_ID'),
            'secret': os.getenv('YANDEX_SECRET'),
            'key': ''
        },
        'SCOPE': ['login:email', 'login:info'],
        'VERIFIED_EMAIL': True,
    }
}


# ---------- НАСТРОЙКИ CELERY ----------
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += [
    'django_celery_beat',
    'django_celery_results',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'GMAIL_USER'
EMAIL_HOST_PASSWORD = 'GMAIL_PASSWORD'
DEFAULT_FROM_EMAIL = "GMAIL_USER"