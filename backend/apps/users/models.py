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

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    # ⭐ auto staff
    def save(self, *args, **kwargs):
        self.is_staff = self.role in ["admin", "manager"]
        super().save(*args, **kwargs)

    # ⭐ property проверки ролей
    @property
    def is_customer(self):
        return self.role == "customer"

    @property
    def is_manager(self):
        return self.role == "manager"

    @property
    def is_admin(self):
        return self.role == "admin"
