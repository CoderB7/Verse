from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from bot.models import TelegramUser

class CustomUser(AbstractUser):
    telegram_user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, related_name='django_user')
