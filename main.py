from ctypes import *
from dotenv import load_dotenv
import os
import requests
from configparser import ConfigParser 

configuration= ConfigParser()
configuration.read('settings.ini')
load_dotenv()

SECRET_KEY = os.getenv("UNSPLASH_SECRET_KEY")
ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
BASE_PATH = configuration.get('DEFAULT', 'base_path')
WALLPAPER_NAME = "wallpaper" + configuration.get('DEFAULT', 'current_wallpaper_number') + ".jpg"
MAX_WALLPAPER_COUNT = int(configuration.get('DEFAULT', 'max_wallpaper_count'))

API_URL = f"https://api.unsplash.com/photos/?client_id={ACCESS_KEY}"

def add_new_wallpaper():
    rand_photo = requests.get(f"https://api.unsplash.com/photos/random?client_id={ACCESS_KEY}&query=nature&orientation=landscape&featured").json()
    photo = rand_photo["links"]["download"]
    
    with open(os.path.join(BASE_PATH, WALLPAPER_NAME), "wb") as f:
        f.write(requests.get(photo, stream=True).content)

def change_wallpaper(image_path: str):
    SPI_SETDESKWALLPAPER = 20
    windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path , 0)

def set_new_wallpaper():
    add_new_wallpaper()
    full_picture_path = os.path.join(BASE_PATH, WALLPAPER_NAME)
    change_wallpaper(full_picture_path)
    configuration['DEFAULT']['current_wallpaper_number'] = str((int(configuration['DEFAULT']['current_wallpaper_number']) + 1) % MAX_WALLPAPER_COUNT)

    with open("settings.ini", "w") as configfile:
        configuration.write(configfile)

set_new_wallpaper()
