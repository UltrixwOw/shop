# config/storage.py
from storages.backends.s3boto3 import S3Boto3Storage
import logging

logger = logging.getLogger(__name__)


class MediaStorage(S3Boto3Storage):
    """Хранилище для медиа-файлов"""
    location = "media"
    file_overwrite = False
    default_acl = 'public-read'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.error(f"🔥 MediaStorage initialized - bucket: {self.bucket_name}, location: {self.location}")


class StaticStorage(S3Boto3Storage):
    """Хранилище для статических файлов"""
    location = "static"
    file_overwrite = True
    default_acl = 'public-read'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.error(f"🔥 StaticStorage initialized - bucket: {self.bucket_name}, location: {self.location}")