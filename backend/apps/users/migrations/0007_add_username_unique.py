# users/migrations/0007_add_username_unique.py
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_username'),
    ]

    operations = [
        # Добавляем уникальность
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                max_length=150,
                unique=True,
                blank=True,
                help_text="Username from email (part before @)"
            ),
        ),
    ]