# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "username"]  # Добавляем username
        extra_kwargs = {
            'username': {'required': False}  # Делаем необязательным
        }

    def create(self, validated_data):
        # Если username не передан, он сгенерируется в менеджере
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "is_verified"]  # Добавляем username
        read_only_fields = ["id", "is_verified"]