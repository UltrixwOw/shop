from .base import *

DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com"]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.com",
]