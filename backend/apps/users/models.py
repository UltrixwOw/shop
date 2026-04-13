# apps/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("manager", "Manager"),
        ("admin", "Admin"),
    ]

    email = models.EmailField(unique=True)
    
    # Добавляем поле username
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,  # Можно оставить пустым при создании
        help_text="Username from email (part before @)"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    is_active = models.BooleanField(default=True) # False default
    is_verified = models.BooleanField(default=True) # False default
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # username не требуется при createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Автоматически генерируем username из email если не указан
        if not self.username and self.email:
            self.username = self.email.split('@')[0]
        
        self.is_staff = self.role in ["admin", "manager"]
        super().save(*args, **kwargs)

    @property
    def is_customer(self):
        return self.role == "customer"

    @property
    def is_manager(self):
        return self.role == "manager"

    @property
    def is_admin(self):
        return self.role == "admin"