from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = [
    "meloni-backend.onrender.com",
    "meloni-frontend.onrender.com",
]

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    "https://meloni-frontend.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://meloni-frontend.onrender.com"
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
SESSION_COOKIE_SAMESITE = 'Lax'  # или 'None' если нужно
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True  # True только для HTTPS
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Безопасное получение DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # fallback для локальной разработки
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }