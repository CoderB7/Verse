import requests

import os
from dotenv import load_dotenv


load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_BOT')
channel_id = '-1002150737533'
channel_id_s = []


def send_message(message) -> None:
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {
        'chat_id': channel_id,
        'text': message
    }
    response = requests.post(url, data=payload)

    # Checking the response
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(f"Response: {response.json()}")
