from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        
        # Автоматически генерируем username из email если не передан
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = email.split('@')[0]

        # Устанавливаем значения по умолчанию
        extra_fields.setdefault("is_active", True) # False
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        # Для обычных пользователей роль по умолчанию - customer
        if 'role' not in extra_fields:
            extra_fields['role'] = 'customer'

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        # Для суперпользователя устанавливаем специальные значения
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")  # Суперпользователь - admin
        extra_fields.setdefault("is_verified", True)  # Суперпользователь сразу верифицирован
        
        # Генерируем username если не передан
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = email.split('@')[0]

        # Проверки для суперпользователя
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
    def create_manager(self, email, password=None, **extra_fields):
        """Вспомогательный метод для создания менеджера"""
        extra_fields.setdefault("role", "manager")
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)  # Менеджеры имеют is_staff=True
        
        return self.create_user(email, password, **extra_fields)