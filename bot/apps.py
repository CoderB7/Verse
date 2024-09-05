from django.apps import AppConfig
from telegram import Bot
from telegram.error import RetryAfter
from django.conf import settings
import time

TELEGRAM_WEBHOOK_URL = 'https://a24a-94-158-60-69.ngrok-free.app'

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        import bot.signals
        # Setting up webhook on startup
        bot = Bot(token=f"{settings.TOKEN_BOT}")
        
        try:
            # Check if the webhook is already set
            current_webhook = bot.getWebhookInfo().url
            expected_webhook = f"{TELEGRAM_WEBHOOK_URL}/bot/webhook/"
            if current_webhook != expected_webhook:
                bot.setWebhook(url=expected_webhook)
        except RetryAfter as e:
            print(f"Rate limit exceeded. Retry in {e.retry_after} seconds.")
            time.sleep(e.retry_after+1)
            bot.setWebhook(url=f"{TELEGRAM_WEBHOOK_URL}/bot/webhook/")

