from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    "meloni-backend.onrender.com",
    "meloni-frontend.onrender.com",
    "melonishop.cc",
    "www.melonishop.cc"
]

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    "https://meloni-frontend.onrender.com",
    "https://melonishop.cc",
    "https://www.melonishop.cc"
]

CSRF_TRUSTED_ORIGINS = [
    "https://meloni-frontend.onrender.com",
    "https://melonishop.cc",
    "https://www.melonishop.cc"
]

CORS_ALLOW_CREDENTIALS = True

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

# Настройки сессий и куки
SESSION_COOKIE_SAMESITE = 'None'  # или 'None' если нужно Lax для единого адреса
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True  # True только для HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = None  # Можно оставить None
CSRF_COOKIE_DOMAIN = None

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')