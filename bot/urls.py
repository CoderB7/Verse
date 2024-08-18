from django.urls import path
from .views import TelegramWebhookView
from bot.authentication.views import otp_login

urlpatterns = [
    path('webhook/', TelegramWebhookView.as_view(), name='webhook'),
    path('otp-login/', otp_login, name='otp_login'),
]
