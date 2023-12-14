from ..image import Image
import requests
import base64
import numpy as np
import io
from PIL import Image as IMG
import os


ADDED_URL = "https://getfile.dokpub.com/yandex/get/"


def download_image(url):
    response = requests.get(url)
    print(response.headers)
    # file = open('image.png', 'wb')
    # file.write(response.content)
    print(response.headers.keys())


def download_array(url):
    # path_orig = 
    response = requests.get(url)
    print(response.headers.keys())
    file = open('save_img.npy', 'wb')
    file.write(response.content)
    img = Image(data=np.load('save_img.npy'))
    img.show()
    return img







def parse_json_file(data: dict) -> Image:
    original_image_path  = os.path.join('data', 'input', data['image_tag'] + '.npy')
    annotated_image_path = os.path.join('data', 'input', data['image_tag'] + '_annotated.npy')
    """
    if data['image_tag'] + '.npy' not in os.listdir(os.path.join('data', 'input')):
        print(f'Download original image...')
        original_image  = requests.get(ADDED_URL + data['original_image_url'] ).content
        print(f'Download annotated image...')
        annotated_image = requests.get(ADDED_URL + data['annotated_image_url']).content
        with open(original_image_path, 'wb') as f:
            f.write(original_image)
        with open(annotated_image_path, 'wb') as f:
            f.write(annotated_image)
    else:
        print('Image found in cash...')
    """
    img = Image(data=np.load(original_image_path))
    return img
    


if __name__ == "__main__":
    # add_url = "https://getfile.dokpub.com/yandex/get/"
    url = 'https://disk.yandex.ru/i/fomDZJWMSmka1Q'

    url_np = 'https://disk.yandex.ru/d/q4nc_JjE8goTgA'
    download_array(ADDED_URL+url_np)