from .base import *

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # временно
    }
}

# config/settings/dev.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']  # или ['127.0.0.1', 'localhost']

# Разрешаем все CORS для разработки
CORS_ALLOW_ALL_ORIGINS = True  # для разработки

# ИЛИ конкретные origins (более безопасно):
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Важно для работы с credentials (cookies, авторизация)
CORS_ALLOW_CREDENTIALS = True

# Добавьте эти настройки если нужно
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Настройки CSRF для кросс-доменных запросов
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Настройки сессий и куки
SESSION_COOKIE_SAMESITE = 'Lax'  # или 'None' если нужно
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False  # True только для HTTPS
CSRF_COOKIE_SECURE = False

# Channels для разработки
ASGI_APPLICATION = "config.asgi.application"
