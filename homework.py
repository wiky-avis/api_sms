import time

import requests
from twilio.rest import Client

import os
from dotenv import load_dotenv 
load_dotenv()


token = os.getenv('TOKEN_VK')
account_sid = os.getenv('ACCOUNT_SID')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')

client = Client(account_sid, token)
# 1. отправляйте SMS-уведомление, когда определённый пользователь ВК появится 
#   в сети
# 2. Методом users.get получите статус пользователя в ВК
# 3. Если пользователь онлайн — отправьте SMS посредством класса Client() из 
#   библиотеки twilio.rest А если пользователь оффлайн — запросите его статус 
# через некоторое время. Метод time.sleep() вас выручит
# 4. Номера телефонов храните в .env в переменных NUMBER_FROM и NUMBER_TO.
def get_status(user_id):
    params = {
            'user_ids': user_id,
            'fields': 'online,verified',
            'access_token': token,
            'v': '5.126'
    }
    
    friends_online = requests.post(
        'https://api.vk.com/method/users.get', params=params
        )
    return friends_online.json()['response']  #Верните статус пользователя в ВК


def sms_sender(sms_text):
    sms_text = client.messages.create(
        body='Сообщение от YandexPraktikum',
        from_=number_from,
        to=number_to
        )
    return sms_text.sid  # Верните sid отправленного сообщения из Twilio


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
