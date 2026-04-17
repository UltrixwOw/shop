from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import logging

logger = logging.getLogger(__name__)


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    default_acl = None


class StaticStorage(S3Boto3Storage):
    location = "static"
    file_overwrite = True
    default_acl = None


# На проде (DEBUG=False) — S3, на локалке — локальное хранилище
if settings.DEBUG:
    media_storage = FileSystemStorage(
        location=settings.MEDIA_ROOT,
        base_url=settings.MEDIA_URL
    )
    static_storage = FileSystemStorage(
        location=settings.STATIC_ROOT,
        base_url=settings.STATIC_URL
    )
else:
    media_storage = MediaStorage()
    static_storage = StaticStorage()