from telegram import Update
from telegram.ext import CallbackContext

from django.conf import settings

from account.models import CustomUser
from .models import TelegramChatInfo, TelegramUser, OTP
import random

from telegram import Update
from telegram.ext import CallbackContext

from django.utils import timezone
from django.conf import settings
from django.core.files import File

from utils.decorators import get_user
from pathlib import Path

import json

def handle_new_member(update: Update, context: CallbackContext, user=CustomUser):
    print(update)
    bot = context.bot
    chat_member = update.my_chat_member
    try:
        chat_member = json.loads(chat_member.to_json())
        from_user = chat_member['from']['username']
        new_status = chat_member["new_chat_member"]["status"]
        print(new_status) 
        if new_status == "administrator":
            
            chat_info = {}
            chat_id = chat_member["chat"]["id"]
            chat_title = chat_member["chat"]["title"]
            chat_type = chat_member["chat"]["type"]
            print(f"Bot added to chat: {chat_title}\nID: {chat_id}")
            print(chat_id)
            try:
                chat_info = bot.get_chat(int(chat_id))
            except Exception as e:
                print(f"Error accessing chat ID {chat_id}: {e}")
            else:
                if chat_info.photo:
                    big_photo_file_id = chat_info.photo.big_file_id
                    if big_photo_file_id:
                        # Now you can use these file_ids to get the actual photo file
                        big_photo = bot.get_file(big_photo_file_id)

                        filename = f"channel_photos/{chat_title}.jpg"
                        file_path = Path('media') / filename

                        # Download the file
                        big_photo.download(custom_path=str(file_path))
                else:
                    # TODO: default image for the channel with no photo  
                    pass
            telegram_user = TelegramUser.objects.get(username=from_user)
            chat_info_instance, created = TelegramChatInfo.objects.get_or_create(
                user=telegram_user,
                chat_id=chat_id, 
                chat_title=chat_title,
                chat_type=chat_type,
            )

            with file_path.open('rb') as f:
                chat_info_instance.photo.save(file_path.name, File(f), save=True)
    
        elif new_status == 'kicked' or new_status == "left":
            chat_id = chat_member["chat"]["id"] 

            try:
                chat_object = TelegramChatInfo.objects.get(chat_id=chat_id)
                chat_object.delete()
            except TelegramChatInfo.DoesNotExist:
                print("The object does not exist.")    
            
    except TypeError or KeyError:
        return None
        

def get_otp(user: TelegramUser):
    now = timezone.now()
    try:
        otp = OTP.objects.filter(active_till__gte=now, user=user).last()

        if otp is None:
            raise OTP.DoesNotExist
    except:
        OTP.objects.filter(user=user).update(active_till=now)
        code = OTP.get_new_code()

        otp = OTP.objects.create(
            user=user,
            active_till=OTP.otp_lifetime(seconds=settings.OTP_EXPIRE_TIME),
            code=code,
        )
    return otp


@get_user
def command_start(
    update: Update, context: CallbackContext, user: TelegramUser
) -> None:
    otp = get_otp(user=user)

    message = (
        f"Salom {user.first_name} 👋\n\n"
        f"[Verse.uz](https://www.verse.uz/) ning rasmiy telegram botiga xush kelibsiz!\n\n"
        f"🔒 *Kodingiz:* ```{otp.code}```\n"
        f"🕔 *Amal qilish muddati:* {otp.lifetime}s"
    )
    update.message.reply_text(message, parse_mode="Markdown")
    update.message.reply_text("Yangi kod olish uchun /start ni yuboring.")

    
