import requests
from django.conf import settings

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')
# WEBHOOK_URL = 'https://74c8-195-158-20-242.ngrok-free.app'


def set_webhook():
    url = f'https://api.telegram.org/bot{TOKEN_BOT}/setWebhook'
    data = {'url': WEBHOOK_URL}
    response = requests.post(url, data=data)
    print(response.json())
    return response.json()


if __name__ == '__main__':
    set_webhook()


