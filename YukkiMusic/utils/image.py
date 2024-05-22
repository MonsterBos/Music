import requests
import json
from config import START_IMG_URL

asyns def gen_image():
    try:
        url = "https://random.imagecdn.app/v1/image?width=1280&height=720&format=json"

        response = requests.get(url)
        data = response.json()
        return data.get("url")
    except Exception:
        return START_IMG_URL

