from Vk import *
from Yandex import *

import requests
import json

with open('token_vk.txt', 'r') as file_object:
    token_vk = file_object.read().strip()

with open('token_yandex.txt', 'r') as file_object:
    token_yandex = file_object.read().strip()

version = '5.126'


def main():
    user_id = input('Введите id пользователя: ') or None
    user_input = input('Введите Yandex токен: ')
    #     token_yandex = user_input
    folder_name = input('Введите имя папки: ')
    photos_number = input('Сколько фотографий сохранить на диск: ')

    with open('token_vk.txt', 'r') as file_object:
        token_vk = file_object.read().strip()

    version = '5.126'

    user = VkUser(token_vk, version, user_id)
    res = user.get_photos()

    i = 0
    while i == 0:
        i = 1
        try:
            upload_to_yandex(res, folder_name, photos_number)
        except requests.HTTPError:
            print('Папка с таким имеменем уже существует')
            i = 0
            user_input = input('Введите имя папки: ')
            folder_name = user_input

    with open('photos.json', 'w') as f:
        json.dump(res[1], f)
        print('Json файл сохранен на диск!')


main()
