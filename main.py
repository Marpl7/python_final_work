import Vk
import Yandex

import json

version = '5.126'


def main():
    user_id = input('Введите id пользователя: ') or None
    token_vk = input('Введите VK токен: ')
    token_yandex = input('Введите Yandex токен: ')
    folder_name = input('Введите имя папки: ')
    photos_number = input('Сколько фотографий сохранить на диск: ')

    user = Vk.VkUser(token_vk, version, user_id)
    res = user.get_photos()

    while True:
        if Yandex.upload_to_yandex(res, token_yandex, folder_name, photos_number) is False:
            print('Папка с таким имеменем уже существует')
            folder_name = input('Введите имя папки: ')
        else:
            Yandex.upload_to_yandex(res, token_yandex, folder_name, photos_number)
            break

    with open('photos.json', 'w') as f:
        json.dump(res[1], f)
        print('Json файл сохранен на диск!')


main()
