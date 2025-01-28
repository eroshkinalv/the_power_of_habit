from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=120, verbose_name="Телефон")
    image = models.ImageField(upload_to="profile_img/", null=True, blank=True, verbose_name="Аватар")

    tg_chat_id = models.CharField(max_length=120, null=True, blank=True, verbose_name="Телеграм chat_id")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
