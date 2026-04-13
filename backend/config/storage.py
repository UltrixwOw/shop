# config/storage.py
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import logging
import traceback
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class MediaStorage(S3Boto3Storage):
    """Хранилище для медиа-файлов (S3)"""
    location = "media"
    file_overwrite = False
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('acl', None)
        
        # Если DEBUG=True - не инициализируем S3
        if settings.DEBUG:
            logger.warning("🔥 MediaStorage: DEBUG=True, using LOCAL storage")
            self._use_local = True
            self._local_storage = FileSystemStorage(
                location=settings.MEDIA_ROOT,
                base_url=settings.MEDIA_URL
            )
            return
        
        self._use_local = False
        logger.info("🔥 MediaStorage: initializing S3 storage")
        try:
            super().__init__(*args, **kwargs)
            self.default_acl = None
            logger.info(f"✅ MediaStorage: S3 initialized - bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"❌ MediaStorage init failed: {e}")
            raise
    
    def _save(self, name, content):
        if self._use_local:
            return self._local_storage._save(name, content)
        return super()._save(name, content)
    
    def exists(self, name):
        if self._use_local:
            return self._local_storage.exists(name)
        try:
            return super().exists(name)
        except:
            return False
    
    def url(self, name):
        if self._use_local:
            return self._local_storage.url(name)
        try:
            return super().url(name)
        except Exception as e:
            logger.error(f"MediaStorage.url failed: {e}")
            return f"{settings.MEDIA_URL}{name}"
    
    def delete(self, name):
        if self._use_local:
            return self._local_storage.delete(name)
        return super().delete(name)


class StaticStorage(S3Boto3Storage):
    """Хранилище для статических файлов (S3)"""
    location = "static"
    file_overwrite = True
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('acl', None)
        
        if settings.DEBUG:
            self._use_local = True
            self._local_storage = FileSystemStorage(
                location=settings.STATIC_ROOT,
                base_url=settings.STATIC_URL
            )
            return
        
        self._use_local = False
        try:
            super().__init__(*args, **kwargs)
            self.default_acl = None
            logger.info(f"✅ StaticStorage: S3 initialized - bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"❌ StaticStorage init failed: {e}")
            raise
    
    def _save(self, name, content):
        if self._use_local:
            return self._local_storage._save(name, content)
        return super()._save(name, content)
    
    def exists(self, name):
        if self._use_local:
            return self._local_storage.exists(name)
        return super().exists(name)
    
    def url(self, name):
        if self._use_local:
            return self._local_storage.url(name)
        return super().url(name)
    
    def delete(self, name):
        if self._use_local:
            return self._local_storage.delete(name)
        return super().delete(name)


# 🔥 Создаем экземпляры для использования в моделях (обратная совместимость)
if settings.DEBUG:
    # В режиме разработки - локальное хранилище
    from django.core.files.storage import default_storage
    media_storage = default_storage
    static_storage = default_storage
    logger.info("✅ Using LOCAL storage (DEBUG mode)")
else:
    # В production - S3
    try:
        media_storage = MediaStorage()
        static_storage = StaticStorage()
        logger.info("✅ Using S3 storage (PRODUCTION mode)")
    except Exception as e:
        logger.error(f"❌ Failed to create S3 storage, falling back to local: {e}")
        from django.core.files.storage import default_storage
        media_storage = default_storage
        static_storage = default_storage