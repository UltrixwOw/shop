from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    "meloni-backend.onrender.com",
    "meloni-frontend.onrender.com",
    "melonishop.cc",
    "www.melonishop.cc"
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

# storage

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = "public-read"
AWS_S3_FILE_OVERWRITE = False

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

DEFAULT_FILE_STORAGE = "config.storage.MediaStorage"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"