from telegram import Update, Bot
from telegram.ext import Updater, Dispatcher, CallbackContext, CommandHandler, ChatMemberHandler

from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import TelegramChatInfo
from django.contrib.auth.mixins import LoginRequiredMixin

from .handlers import handle_new_member, command_start

from celery import shared_task
import os
from dotenv import load_dotenv

import json
import logging

load_dotenv()

logger = logging.getLogger(__name__)

bot = Bot(token=f"{settings.TOKEN_BOT}")

dispatcher = Dispatcher(bot, update_queue=None, workers=4)
dispatcher.add_handler(ChatMemberHandler(handle_new_member, pass_chat_data=True))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
dispatcher.add_handler(CommandHandler("start", command_start))


@method_decorator(csrf_exempt, name="dispatch")
class TelegramWebhookView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        update = Update.de_json(json.loads(request.body.decode("utf-8")), bot)
        print(update)
        try:
            dispatcher.process_update(update)
        except TypeError:
            dispatcher.process_update(update)
            
        return JsonResponse({"ok": True})

    def get(self, *args, **kwargs):
        return JsonResponse({"ok": True}, status=204)

@shared_task
def send_message(chat_id, title, content):
    message = f"**{title}**\n\n{content}"
    
    try:
        sent_message = bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        message_id = sent_message.message_id
        print(message_id)
        logger.info(f"Message sent to chat_id {chat_id}: {message}")
        return message_id
    except Exception as e:
        logger.error(f"Failed to send message to chat_id {chat_id}: {e}")
        return False

@shared_task
def update_message(chat_id, telegram_message_id, title, content):
    message = f"**{title}**\n\n{content}"

    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=telegram_message_id,
            text=message,
            parse_mode='Markdown'
        )
        return True
    except Exception as e:
        return False
