from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import logging
import traceback

logger = logging.getLogger(__name__)

logger.error("🚀 STORAGE.PY LOADED")
logger.error(f"🚀 DEBUG VALUE AT IMPORT: {settings.DEBUG}")

# ==========================================
# LOCAL STORAGE (только для разработки)
# ==========================================

class LocalMediaStorage(FileSystemStorage):
    """Локальное хранилище для медиа-файлов (только DEBUG=True)"""
    def __init__(self, *args, **kwargs):
        super().__init__(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL
        )

class LocalStaticStorage(FileSystemStorage):
    """Локальное хранилище для статических файлов (только DEBUG=True)"""
    def __init__(self, *args, **kwargs):
        super().__init__(
            location=settings.STATIC_ROOT,
            base_url=settings.STATIC_URL
        )


# ==========================================
# MEDIA STORAGE (S3)
# ==========================================

class MediaStorage(S3Boto3Storage):
    """S3 хранилище для медиа-файлов"""
    location = "media"
    file_overwrite = False
    default_acl = None  # Не отправляем ACL заголовки
    
    def __init__(self, *args, **kwargs):
        # Убираем acl из kwargs
        kwargs.pop('acl', None)
        
        logger.error("🔥 MediaStorage: initializing S3...")
        logger.error(f"🔥 AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
        logger.error(f"🔥 AWS_S3_REGION_NAME: {settings.AWS_S3_REGION_NAME}")
        
        try:
            super().__init__(*args, **kwargs)
            logger.error(f"✅ MediaStorage: S3 initialized successfully")
        except Exception as e:
            logger.error(f"❌ MediaStorage: S3 init failed: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def _save(self, name, content):
        """Сохраняет файл в S3"""
        try:
            return super()._save(name, content)
        except Exception as e:
            logger.error(f"❌ MediaStorage._save error: {e}")
            raise
    
    def url(self, name):
        """Возвращает URL файла в S3"""
        return super().url(name)


# ==========================================
# STATIC STORAGE (S3)
# ==========================================

class StaticStorage(S3Boto3Storage):
    """S3 хранилище для статических файлов"""
    location = "static"
    file_overwrite = True
    default_acl = None
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('acl', None)
        
        logger.error("🔥 StaticStorage: initializing S3...")
        
        try:
            super().__init__(*args, **kwargs)
            logger.error(f"✅ StaticStorage: S3 initialized successfully")
        except Exception as e:
            logger.error(f"❌ StaticStorage: S3 init failed: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def _save(self, name, content):
        return super()._save(name, content)
    
    def url(self, name):
        return super().url(name)


# ==========================================
# ВЫБОР СТОРАДЖА В ЗАВИСИМОСТИ ОТ DEBUG
# ==========================================

logger.error(f"🔥 FINAL DEBUG VALUE: {settings.DEBUG}")

if settings.DEBUG:
    logger.error("✅ USING LOCAL STORAGE (DEBUG mode)")
    # На локалке используем локальное хранилище
    media_storage = LocalMediaStorage()
    static_storage = LocalStaticStorage()
else:
    logger.error("✅ USING S3 STORAGE (PRODUCTION mode)")
    # На проде используем S3
    media_storage = MediaStorage()
    static_storage = StaticStorage()

logger.error(f"✅ media_storage class: {media_storage.__class__.__name__}")
logger.error(f"✅ static_storage class: {static_storage.__class__.__name__}")