from django.db import models
from django.utils.text import slugify
import random

from django.utils import timezone
from common.models import BaseModel


class TelegramUser(BaseModel):
    user_id = models.PositiveBigIntegerField(unique=True)

    username = models.CharField(max_length=256, null=True, blank=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"


class OTP(BaseModel):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    code = models.CharField(max_length=6)
    active_till = models.DateTimeField(editable=False)

    @property
    def lifetime(self):
        time = self.active_till - timezone.now()
        return time.seconds

    @classmethod
    def get_new_code(cls):
        code = random.randint(100000, 999999)
        while OTP.objects.filter(code=code, active_till__gte=timezone.now()).exists():
            code = random.randint(100000, 999999)
        return str(code)

    @classmethod
    def otp_lifetime(cls, seconds):
        return timezone.now() + timezone.timedelta(seconds=seconds)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"


class TelegramChatInfo(BaseModel):
    user = models.ForeignKey(to=TelegramUser, on_delete=models.CASCADE, blank=True, null=True)
    chat_id = models.BigIntegerField(blank=True)
    chat_title = models.CharField(max_length=256)
    chat_type = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='channel_photos/', null=True, blank=True)
    
    slug = models.SlugField(max_length=250, blank=True)

    def __str__(self):
        return self.chat_title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.chat_title)
        super().save(*args, **kwargs)

