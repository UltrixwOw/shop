# config/settings/prod.py
from .base import *

import os
import logging

logger = logging.getLogger(__name__)

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

SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ==========================================
# S3 STORAGE SETTINGS
# ==========================================

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "eu-central-1")

# Отладка
logger.error(f"🔥 AWS_ACCESS_KEY_ID: {'SET' if AWS_ACCESS_KEY_ID else 'NOT SET'}")
logger.error(f"🔥 AWS_SECRET_ACCESS_KEY: {'SET' if AWS_SECRET_ACCESS_KEY else 'NOT SET'}")
logger.error(f"🔥 AWS_STORAGE_BUCKET_NAME: {AWS_STORAGE_BUCKET_NAME}")
logger.error(f"🔥 AWS_S3_REGION_NAME: {AWS_S3_REGION_NAME}")

# S3 конфигурация
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = "public-read"
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False

if AWS_STORAGE_BUCKET_NAME and AWS_S3_REGION_NAME:
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
    
    # ВАЖНО: переопределяем URL и хранилища
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    
    DEFAULT_FILE_STORAGE = "config.storage.MediaStorage"
    STATICFILES_STORAGE = "config.storage.StaticStorage"
    
    logger.error(f"🔥 S3 CONFIGURED - STATIC URL: {STATIC_URL}")
    logger.error(f"🔥 S3 CONFIGURED - MEDIA URL: {MEDIA_URL}")
else:
    # Fallback на локальное хранилище (не должно быть в production)
    logger.error("🔥 S3 NOT CONFIGURED - USING LOCAL STORAGE")
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")