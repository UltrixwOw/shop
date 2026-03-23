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
        # Гарантированно убираем ACL из параметров
        kwargs['default_acl'] = None
        kwargs['acl'] = None  # явно отключаем
        
        logger.error(f"🔥 MediaStorage.__init__ START - ACL disabled")
        try:
            super().__init__(*args, **kwargs)
            logger.error(f"🔥 MediaStorage initialized SUCCESS - bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"🔥🔥🔥 MediaStorage.__init__ FAILED: {type(e).__name__} - {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _save(self, name, content):
        """Перехватываем сохранение и принудительно удаляем ACL"""
        logger.error(f"🔥 MediaStorage._save called for: {name}")
        
        # Получаем параметры и гарантированно удаляем ACL
        extra_args = self._get_write_parameters(name, content)
        if 'ACL' in extra_args:
            del extra_args['ACL']
            logger.error(f"🔥 Removed ACL from extra_args")
        
        logger.error(f"🔥 Extra args: {extra_args}")
        
        try:
            # Сохраняем файл вручную, минуя стандартный _save
            obj = self.bucket.Object(self._encode_name(self._clean_name(name)))
            obj.upload_fileobj(content, ExtraArgs=extra_args)
            logger.error(f"🔥 MediaStorage._save SUCCESS: {name}")
            return name
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_msg = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f"🔥🔥🔥 AWS CLIENT ERROR - Code: {error_code}, Message: {error_msg}")
            logger.error(traceback.format_exc())
            raise
        except Exception as e:
            logger.error(f"🔥🔥🔥 MediaStorage._save FAILED: {type(e).__name__} - {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _get_write_parameters(self, name, content):
        """Получаем параметры записи и удаляем ACL"""
        params = super()._get_write_parameters(name, content)
        # Удаляем ACL из параметров
        if 'ACL' in params:
            del params['ACL']
        return params
    
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


class StaticStorage(S3Boto3Storage):
    """Хранилище для статических файлов"""
    location = "static"
    file_overwrite = True
    
    def __init__(self, *args, **kwargs):
        kwargs['default_acl'] = None
        kwargs['acl'] = None
        try:
            super().__init__(*args, **kwargs)
            logger.error(f"🔥 StaticStorage initialized - bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"🔥🔥🔥 StaticStorage.__init__ FAILED: {type(e).__name__} - {str(e)}")
            raise
    
    def _save(self, name, content):
        extra_args = self._get_write_parameters(name, content)
        if 'ACL' in extra_args:
            del extra_args['ACL']
        try:
            obj = self.bucket.Object(self._encode_name(self._clean_name(name)))
            obj.upload_fileobj(content, ExtraArgs=extra_args)
            return name
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_msg = e.response.get('Error', {}).get('Message', str(e))
            logger.error(f"🔥🔥🔥 AWS CLIENT ERROR (Static): {error_code} - {error_msg}")
            raise
    
    def _get_write_parameters(self, name, content):
        params = super()._get_write_parameters(name, content)
        if 'ACL' in params:
            del params['ACL']
        return params


# Создаём экземпляр
try:
    media_storage = MediaStorage()
    logger.error(f"🔥 media_storage instance created successfully")
except Exception as e:
    logger.error(f"🔥🔥🔥 FAILED to create media_storage instance: {e}")
    media_storage = None