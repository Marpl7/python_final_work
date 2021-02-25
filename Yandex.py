import requests
import time
from tqdm import tqdm


class YaUploader:
    def __init__(self, token_yandex: str):
        self.token_yandex = token_yandex

    def upload(self, folder_name, file_name, file):
        """Метод загружает файл file на яндекс диск"""
        TOKEN = self.token_yandex
        HEADERS = {
            'Authorization': f'OAuth {TOKEN}'
        }

        response = requests.get(
            'https://cloud-api.yandex.net/v1/disk/resources/upload',
            params={
                'path': str(folder_name + '/' + file_name),
                'overwrite': True
            },
            headers=HEADERS
        )

        response.raise_for_status()

        href = response.json()['href']

        upload_response = requests.put(href, files={'file': file})
        upload_response.raise_for_status()

    def create_folder(self, folder_name):
        """Метод создает папку folder_name на яндекс диск"""

        TOKEN = self.token_yandex
        HEADERS = {
            'Authorization': f'OAuth {TOKEN}'
        }

        response = requests.put(
            'https://cloud-api.yandex.net/v1/disk/resources',
            params={
                'path': str(folder_name)

            },
            headers=HEADERS
        )

        response.raise_for_status()


""""Загружает файлы на Yandex Disk, по умолчанию папка для загрузки - vk_photos, кол-во фотографий = 5"""


def upload_to_yandex(photos, token_yandex, folder_name='vk_photos', photos_number=5):
    photos_urls = photos[0]
    file_names = [file['file_name'] for file in photos[1]]

    if photos_number == '':
        photos_number = 5
    elif int(photos_number) > len(photos_urls):
        print(f'Максимальное количество файлов для загрузки {len(photos_urls)}')
        photos_number = len(photos_urls)
    elif int(photos_number) == 0:
        print('Выбрано 0 файлов для загрузки')
        return

    photos_urls = photos_urls[0:int(photos_number)]

    uploader = YaUploader(token_yandex)

    if folder_name == '':
        folder_name = 'vk_photos'

    try:
        uploader.create_folder(folder_name)
    except requests.HTTPError:
        return False

    i = 0

    for urls in tqdm(photos_urls, desc='Uploading photos to Yandex Disc'):
        file_response = requests.get(urls[0])
        file_name = file_names[i]
        uploader.upload(folder_name, file_name, file_response.content)
        # print(f'Файл {file_name} успешно загружен!')
        i += 1
        time.sleep(0.1)
