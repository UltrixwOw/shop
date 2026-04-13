# apps/shop/models.py
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Avg
from django.core.files.storage import default_storage
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
        related_name='products'
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
        # Убираем storage=media_storage - используем default_storage
        validators=[validate_image_size]
    )
    
    thumbnail = models.ImageField(
        upload_to="products/thumbnails/%Y/%m/",
        blank=True,
        null=True
        # Убираем storage=media_storage - используем default_storage
    )

    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_main", "created_at"]
        
    def save(self, *args, **kwargs):
        logger.error(f"🔥 FIELD STORAGE: {self.image.storage.__class__}")
        logger.error(f"🔥 IMAGE NAME BEFORE SAVE: {self.image.name}")

        with transaction.atomic():
            # 1️⃣ main image
            if not self.product.images.filter(is_main=True).exclude(id=self.id).exists():
                self.is_main = True

            if self.is_main:
                self.product.images.filter(is_main=True).exclude(id=self.id).update(is_main=False)

            # 👉 СНАЧАЛА сохраняем объект (важно для S3)
            super().save(*args, **kwargs)

            # 2️⃣ обработка изображения
            if self.image:
                img = Image.open(self.image)

                img.thumbnail((1200, 1200), Image.LANCZOS)

                buffer = BytesIO()
                img.save(buffer, format="WEBP", quality=85)

                base_name = os.path.splitext(os.path.basename(self.image.name))[0]
                file_name = f"{base_name}.webp"

                self.image.save(
                    file_name,
                    ContentFile(buffer.getvalue()),
                    save=False
                )

                # 3️⃣ thumbnail
                thumb = Image.open(BytesIO(buffer.getvalue()))
                thumb.thumbnail((400, 400), Image.LANCZOS)

                thumb_buffer = BytesIO()
                thumb.save(thumb_buffer, format="WEBP", quality=80)

                thumb_name = f"{base_name}_thumb.webp"

                self.thumbnail.save(
                    thumb_name,
                    ContentFile(thumb_buffer.getvalue()),
                    save=False
                )

                # 👉 сохраняем обновлённые поля
                super().save(update_fields=["image", "thumbnail"])
        
    def __str__(self):
        return f"Image for {self.product.name}"