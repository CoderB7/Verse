import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .signals import send_message

class TelegramInfoConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None 


    async def connect(self):
        self.user = self.scope['user']
        
        if self.user.is_anonymous:
            print('closing')
            self.close()
        else:
            await self.channel_layer.group_add(
                'public_room',
                self.channel_name,
            )

            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'public_room', 
            self.channel_name,
        )
    
    async def send_info(self, event):
        await self.send(text_data=json.dumps({'data': event}))


# for sending posts to Telegram channel asynchronously
# no need to add to public group
class BackgroundTaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # You can perform any setup if needed
        await self.accept()

    async def disconnect(self, close_code):
        # Handle disconnection cleanup if needed
        pass

    async def send_telegram_message(self, event):
        print('received')
        chat_id = event['chat_id']
        title = event['title']
        content = event['content']
        # Call the asynchronous send_message function
        success = await send_message(chat_id, title, content)
        if success:
            print("Message sent successfully.")
        else:
            print("Failed to send message.")

