import requests

import os
from dotenv import load_dotenv

import sys

load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')


def delete_webhook():
    delete_url = f"https://api.telegram.org/bot{TOKEN_BOT}/deleteWebhook"
    response = requests.get(delete_url)

    if response.status_code == 200:
        return 'True'
    else:
        return 'False'


if __name__ == '__main__':
    status = delete_webhook()
    sys.exit(status)

