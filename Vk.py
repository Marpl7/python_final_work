import requests


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token_vk, version, user_id=None):
        self.user_id = user_id
        self.token_vk = token_vk
        self.version = version
        self.params = {
            'user_id': self.user_id,
            'access_token': self.token_vk,
            'v': self.version
        }

        if self.user_id is None:
            self.user_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def get_photos(self):

        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': 1

        }
        res = requests.get(photos_url, params={**self.params, **photos_params})

        res = res.json()['response']['items']

        likes = []
        urllist = []
        photos = []

        for photo in res:
            urls = photo['sizes'][-1]['url']
            urllist.append([urls])
            file_name = photo['likes']['count']
            file_size = photo['sizes'][-1]['type']
            file_date = photo['date']
            if file_name in likes:
                file_name = str(file_name) + '_' + str(file_date) + '.jpg'
            else:
                likes.append(file_name)
                file_name = str(file_name) + '.jpg'

            photos.append({'file_name': file_name, 'size': file_size})

        return urllist, photos
