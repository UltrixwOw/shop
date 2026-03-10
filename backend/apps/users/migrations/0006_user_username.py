# users/migrations/0006_add_username_field.py
from django.db import migrations, models


def set_username_from_email(apps, schema_editor):
    User = apps.get_model('users', 'User')
    for user in User.objects.all():
        if not user.username:
            # Берем часть email до @
            username = user.email.split('@')[0]
            # Проверяем уникальность, добавляем суффикс если нужно
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_role'),  # Укажите правильную предыдущую миграцию
    ]

    operations = [
        # Добавляем поле без unique
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(
                max_length=150,
                blank=True,
                null=True,  # Разрешаем NULL временно
                help_text="Username from email (part before @)"
            ),
        ),
        # Заполняем username для существующих пользователей
        migrations.RunPython(set_username_from_email),
        # Меняем поле на NOT NULL
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                max_length=150,
                blank=True,
                help_text="Username from email (part before @)"
            ),
        ),
    ]