from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/message/', consumers.BackgroundTaskConsumer.as_asgi()),
    re_path(r'ws/info/', consumers.TelegramInfoConsumer.as_asgi()),
]


