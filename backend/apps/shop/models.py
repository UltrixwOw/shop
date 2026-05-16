# apps/shop/models.py

from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Avg
from config.storage import media_storage

import os
import logging

logger = logging.getLogger(__name__)


def validate_image_size(image):
    max_size_mb = 5

    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError("Максимальный размер файла 5MB")


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def rating(self):
        return self.reviews.filter(
            is_approved=True
        ).aggregate(
            Avg("rating")
        )["rating__avg"]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="products/%Y/%m/",
        storage=media_storage,
        validators=[validate_image_size]
    )

    thumbnail = models.ImageField(
        upload_to="products/thumbnails/%Y/%m/",
        storage=media_storage,
        blank=True,
        null=True
    )

    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_main", "created_at"]

    def save(self, *args, **kwargs):
        logger.error(
            f"🔥 STORAGE CLASS: {self.image.storage.__class__.__name__}"
        )

        with transaction.atomic():

            # =============================
            # MAIN IMAGE
            # =============================

            if not self.product.images.filter(
                is_main=True
            ).exclude(id=self.id).exists():
                self.is_main = True

            if self.is_main:
                self.product.images.filter(
                    is_main=True
                ).exclude(id=self.id).update(is_main=False)

            super().save(*args, **kwargs)

            # =============================
            # PROCESS IMAGE
            # =============================

            if self.image:
                img = Image.open(self.image)

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                img.thumbnail((1200, 1200), Image.LANCZOS)

                buffer = BytesIO()

                img.save(
                    buffer,
                    format="WEBP",
                    quality=85
                )

                buffer.seek(0)

                # =============================
                # MAIN FILE NAME
                # =============================

                original_name = os.path.basename(self.image.name)
                base_name = os.path.splitext(original_name)[0]

                image_filename = f"{base_name}.webp"

                # ⚠️ ВАЖНО:
                # НЕ передаём полный путь products/...
                # upload_to сделает путь автоматически

                self.image.save(
                    image_filename,
                    ContentFile(buffer.getvalue()),
                    save=False
                )

                # =============================
                # THUMBNAIL
                # =============================

                thumb = Image.open(BytesIO(buffer.getvalue()))

                thumb.thumbnail((400, 400), Image.LANCZOS)

                thumb_buffer = BytesIO()

                thumb.save(
                    thumb_buffer,
                    format="WEBP",
                    quality=80
                )

                thumb_buffer.seek(0)

                thumb_filename = f"{base_name}_thumb.webp"

                # ⚠️ НЕ products/thumbnails/...
                # upload_to сам добавит путь

                self.thumbnail.save(
                    thumb_filename,
                    ContentFile(thumb_buffer.getvalue()),
                    save=False
                )

                super().save(update_fields=[
                    "image",
                    "thumbnail"
                ])

    def __str__(self):
        return f"Image for {self.product.name}"