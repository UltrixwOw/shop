from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import logging
import traceback

logger = logging.getLogger(__name__)

logger.error("🚀 STORAGE.PY LOADED")
logger.error(f"🚀 DEBUG VALUE AT IMPORT: {settings.DEBUG}")
logger.error(f"🚀 DJANGO_SETTINGS_MODULE: {getattr(settings, 'SETTINGS_MODULE', 'NO MODULE')}")

# ==========================================
# MEDIA STORAGE
# ==========================================
class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False

    def __init__(self, *args, **kwargs):
        kwargs.pop('acl', None)

        logger.error("🔥 MediaStorage INIT CALLED")
        logger.error(f"🔥 MediaStorage DEBUG: {settings.DEBUG}")

        if settings.DEBUG:
            logger.error("❌ USING LOCAL MEDIA STORAGE (DEBUG=True)")
            self._use_local = True
            self._local_storage = FileSystemStorage(
                location=settings.MEDIA_ROOT,
                base_url=settings.MEDIA_URL
            )
            return

        self._use_local = False

        try:
            logger.error("🔥 INITIALIZING S3 MEDIA STORAGE...")
            super().__init__(*args, **kwargs)
            self.default_acl = None
            logger.error(f"✅ S3 MEDIA OK - bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"❌ S3 MEDIA INIT ERROR: {e}")
            logger.error(traceback.format_exc())
            raise

    def _save(self, name, content):
        if self._use_local:
            return self._local_storage._save(name, content)

        try:
            return super()._save(name, content)
        except Exception as e:
            logger.error("❌ S3 SAVE ERROR:")
            logger.error(str(e))
            import traceback
            logger.error(traceback.format_exc())
            raise

    def url(self, name):
        if self._use_local:
            return self._local_storage.url(name)
        return super().url(name)


# ==========================================
# STATIC STORAGE
# ==========================================
class StaticStorage(S3Boto3Storage):
    location = "static"
    file_overwrite = True

    def __init__(self, *args, **kwargs):
        kwargs.pop('acl', None)

        logger.error("🔥 StaticStorage INIT CALLED")
        logger.error(f"🔥 StaticStorage DEBUG: {settings.DEBUG}")

        if settings.DEBUG:
            logger.error("❌ USING LOCAL STATIC STORAGE (DEBUG=True)")
            self._use_local = True
            self._local_storage = FileSystemStorage(
                location=settings.STATIC_ROOT,
                base_url=settings.STATIC_URL
            )
            return

        self._use_local = False

        try:
            logger.error("🔥 INITIALIZING S3 STATIC STORAGE...")
            super().__init__(*args, **kwargs)
            self.default_acl = None
            logger.error(f"✅ S3 STATIC OK - bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"❌ S3 STATIC INIT ERROR: {e}")
            logger.error(traceback.format_exc())
            raise

    def _save(self, name, content):
        if self._use_local:
            return self._local_storage._save(name, content)
        return super()._save(name, content)

    def url(self, name):
        if self._use_local:
            return self._local_storage.url(name)
        return super().url(name)


# ==========================================
# INIT STORAGE (ВАЖНО)
# ==========================================
logger.error("🔥 INIT GLOBAL STORAGE OBJECTS")

try:
    logger.error(f"🔥 FINAL DEBUG BEFORE STORAGE INIT: {settings.DEBUG}")

    if settings.DEBUG:
        logger.error("❌ GLOBAL: USING LOCAL STORAGE")
        from django.core.files.storage import default_storage
        media_storage = default_storage
        static_storage = default_storage
    else:
        logger.error("✅ GLOBAL: USING S3 STORAGE")
        media_storage = MediaStorage()
        static_storage = StaticStorage()

except Exception as e:
    logger.error(f"❌ GLOBAL STORAGE INIT FAILED: {e}")
    logger.error(traceback.format_exc())
    raise