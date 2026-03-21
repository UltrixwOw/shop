from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import logging

logger = logging.getLogger(__name__)

# Проверка при загрузке модуля
logger.error(f"🔥 AWS BUCKET: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)}")
logger.error(f"🔥 AWS REGION: {getattr(settings, 'AWS_S3_REGION_NAME', None)}")

class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False