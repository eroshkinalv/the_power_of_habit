# Generated by Django 5.1.4 on 2025-01-21 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="tg_chat_id",
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name="Телеграм chat_id"),
        ),
    ]
