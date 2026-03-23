# config/storage.py
from storages.backends.s3boto3 import S3Boto3Storage
import logging
import traceback
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class MediaStorage(S3Boto3Storage):
    """Хранилище для медиа-файлов"""
    location = "media"
    file_overwrite = False
    
    def __init__(self, *args, **kwargs):
        logger.error(f"🔥 MediaStorage.__init__ START")
        try:
            super().__init__(*args, **kwargs)
            logger.error(f"🔥 MediaStorage initialized SUCCESS - bucket: {self.bucket_name}, location: {self.location}")
            logger.error(f"🔥 MediaStorage endpoint: {self.endpoint_url}")
            logger.error(f"🔥 MediaStorage region: {self.region_name}")
        except Exception as e:
            logger.error(f"🔥🔥🔥 MediaStorage.__init__ FAILED: {type(e).__name__} - {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _save(self, name, content):
        """Перехватываем сохранение файла для детального логирования"""
        logger.error(f"🔥 MediaStorage._save called for: {name}")
        logger.error(f"🔥 Content type: {type(content)}")
        logger.error(f"🔥 Content size: {len(content.getvalue()) if hasattr(content, 'getvalue') else 'unknown'} bytes")
        
        try:
            result = super()._save(name, content)
            logger.error(f"🔥 MediaStorage._save SUCCESS: {result}")
            return result
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_msg = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f"🔥🔥🔥 AWS CLIENT ERROR - Code: {error_code}, Message: {error_msg}")
            logger.error(f"🔥🔥🔥 Full response: {e.response}")
            logger.error(traceback.format_exc())
            raise
        except Exception as e:
            logger.error(f"🔥🔥🔥 MediaStorage._save FAILED: {type(e).__name__} - {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def exists(self, name):
        """Логируем проверку существования файла"""
        logger.error(f"🔥 MediaStorage.exists called for: {name}")
        try:
            result = super().exists(name)
            logger.error(f"🔥 MediaStorage.exists result: {result}")
            return result
        except Exception as e:
            logger.error(f"🔥🔥🔥 MediaStorage.exists FAILED: {type(e).__name__} - {str(e)}")
            raise
    
    def url(self, name):
        """Логируем генерацию URL"""
        logger.error(f"🔥 MediaStorage.url called for: {name}")
        try:
            result = super().url(name)
            logger.error(f"🔥 MediaStorage.url result: {result}")
            return result
        except Exception as e:
            logger.error(f"🔥🔥🔥 MediaStorage.url FAILED: {type(e).__name__} - {str(e)}")
            raise


class StaticStorage(S3Boto3Storage):
    """Хранилище для статических файлов"""
    location = "static"
    file_overwrite = True
    
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
            logger.error(f"🔥 StaticStorage initialized - bucket: {self.bucket_name}, location: {self.location}")
        except Exception as e:
            logger.error(f"🔥🔥🔥 StaticStorage.__init__ FAILED: {type(e).__name__} - {str(e)}")
            raise
    
    def _save(self, name, content):
        logger.error(f"🔥 StaticStorage._save called for: {name}")
        try:
            result = super()._save(name, content)
            logger.error(f"🔥 StaticStorage._save SUCCESS: {result}")
            return result
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_msg = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f"🔥🔥🔥 AWS CLIENT ERROR (Static): {error_code} - {error_msg}")
            raise
        except Exception as e:
            logger.error(f"🔥🔥🔥 StaticStorage._save FAILED: {type(e).__name__} - {str(e)}")
            raise


# Создаём экземпляр для использования в моделях
try:
    media_storage = MediaStorage()
    logger.error(f"🔥 media_storage instance created successfully")
except Exception as e:
    logger.error(f"🔥🔥🔥 FAILED to create media_storage instance: {e}")
    media_storage = None