import os
import sys
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True if os.getenv("DEBUG") == "True" else False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "habit_tracker",
    "users",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_celery_beat",
    "django_filters",
    "corsheaders",
    "drf_yasg",
    "multiselectfield",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("HOST"),
        "PORT": os.getenv("PORT"),
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

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = (BASE_DIR / "static",)
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

# Настройки JWT-токенов
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
}

# Настройки CORS (доступ к данным на разных доменах)
CORS_ALLOWED_ORIGINS = [
    os.getenv("CORS_ALLOWED_ORIGINS"),  # Замените на адрес вашего фронтенд-сервера
]

CSRF_TRUSTED_ORIGINS = [
    os.getenv("CORS_ALLOWED_ORIGINS"),  # Замените на адрес вашего фронтенд-сервера
    os.getenv("CSRF_TRUSTED_ORIGINS"),  # и добавьте адрес бэкенд-сервера
]

CORS_ALLOW_ALL_ORIGINS = False

# Настройки для Celery
# URL-адрес брокера сообщений
CELERY_BROKER_URL = 'redis://redis:6379/0'  # Например, Redis, который по умолчанию работает на порту 6379

# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Часовой пояс для работы Celery
CELERY_TIMEZONE = "Europe/Moscow"

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    "check_done": {
        "task": "habit_tracker.tasks.check_done",  # Путь к задаче
        "schedule": crontab(hour=00, minute=00),  # Расписание выполнения задачи (например, каждые 10 минут)
    },
    "check_update": {
        "task": "habit_tracker.tasks.check_update",  # Путь к задаче
        "schedule": crontab(hour=21, minute=00),  # Расписание выполнения задачи (например, каждые 10 минут)
    },
    "check_time": {
        "task": "habit_tracker.tasks.check_time",  # Путь к задаче
        "schedule": timedelta(minutes=1),  # Расписание выполнения задачи (например, каждые 10 минут)
    },
}

CACHE_ENABLED = True if os.getenv('CACHE_ENABLED') == 'True' else False

if CACHE_ENABLED:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': 'redis://redis:6379/1',
        }
    }

TELEGRAM_URL = "https://api.telegram.org/bot"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_ID = os.getenv("TELEGRAM_ID")

if 'test' in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "test_db.sqlite3",
        }
    }
