### WORKED ###

import requests
from django.conf import settings

import os
from dotenv import load_dotenv

import json

load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')


def get_file_path(file_id: int):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/getFile"
    payload = {
        'file_id': file_id,
    }
    response = requests.get(url, data=payload)
    if response.status_code == 200:
        file_path = response.json()['result']['file_path']
        return file_path


def get_file_id(chat_id: int):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/getChat"
    payload = {
        'chat_id': chat_id,
    }
    response = requests.get(url, data=payload)
    if response.status_code == 200:
        # print(response.status_code)
        # print(response.content)
        # print(response.json())
        try:
            file_id = response.json()['result']['photo']['big_file_id']
        except KeyError:
            return 'no_photo'
        return file_id


def get_chat_info(update) -> dict:
    # url = f"https://api.telegram.org/bot{TOKEN_BOT}/getUpdates"
    # response = requests.get(url)
    # update = sys.argv[1]
    update = json.loads(update)
    if update:
        try:
            print(update)
            chat_id = update['my_chat_member']['chat']['id']
            chat_name = update['my_chat_member']['chat']['title']
            chat_type = update['my_chat_member']['chat']['type']
            chat_info = {
                'chat_id': str(chat_id),
                'chat_name': chat_name,
                'chat_type': chat_type,
            }
        except KeyError:
            return None
        return chat_info


def get_chat_photo(chat_id, chat_name):
    file_id = get_file_id(chat_id)
    if file_id == 'no_photo':
        print('no_photo')
        pass
    elif file_id:
        file_path = get_file_path(file_id)
        url = f"https://api.telegram.org/file/bot{TOKEN_BOT}/{file_path}"
        file_response = requests.get(url)
        with open(f'{chat_name}_photo.jpg', mode='wb') as file:
            file.write(file_response.content)



