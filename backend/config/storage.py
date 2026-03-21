from storages.backends.s3boto3 import S3Boto3Storage
import logging

logger = logging.getLogger(__name__)

class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    default_acl = 'public-read'
    
    def __init__(self, *args, **kwargs):
        # Логирование при инициализации, когда settings уже загружены
        from django.conf import settings
        logger.error(f"🔥 MEDIA STORAGE INIT - BUCKET: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)}")
        logger.error(f"🔥 MEDIA STORAGE INIT - REGION: {getattr(settings, 'AWS_S3_REGION_NAME', None)}")
        super().__init__(*args, **kwargs)


class StaticStorage(S3Boto3Storage):
    location = "static"
    file_overwrite = True
    default_acl = 'public-read'
    
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        logger.error(f"🔥 STATIC STORAGE INIT - BUCKET: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)}")
        super().__init__(*args, **kwargs)