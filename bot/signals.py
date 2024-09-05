from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import TelegramChatInfo
from user_verse.models import Post
from .views import send_message
import requests
import asyncio

@receiver(post_save, sender=TelegramChatInfo)
def info_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        django_user = instance.user.django_user
        chat_info = {
            'chat_id': instance.chat_id,
            'chat_title': instance.chat_title,
            'chat_type': instance.chat_type,
        }

        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "send_info",
                "message": chat_info,
                "django_user_id": django_user.id,
            }
        )


# @receiver(post_save, sender=Post)
# def notify_telegram_channel(sender, instance, created, **kwargs):
#     if created: # Ensure the signal is only for new posts
#         if instance.chat:
#             chat_id = instance.chat.chat_id  # Adjust based on your model
#             title = instance.title
#             content = instance.content

#             # Get the channel layer
#             channel_layer = get_channel_layer()
#             print('sending')
#             # Send the message to the channel
#             async_to_sync(channel_layer.send)(
#                 "background-tasks",
#                 {
#                     "type": "send_telegram_message",
#                     "chat_id": chat_id,
#                     "title": title,
#                     "content": content
#                 }
#             )

#         elif instance.blog:
#             pass

@receiver(post_save, sender=Post)
def trigger_send_message(sender, instance, created, **kwargs):
    if created:
        if instance.chat:
            result = send_message.delay(
                instance.chat.chat_id,
                instance.title,
                instance.content,
            )
            message_id = result.get(timeout=20)
            
            Post.objects.filter(id=instance.id).update(telegram_message_id=message_id)


