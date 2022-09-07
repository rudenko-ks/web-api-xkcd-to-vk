import os
import datetime
import requests
from environs import Env
from functions import download_comics


def fetch_comics_and_metadata() -> None:
    comics_folder_path = "files"
    comics_name_template = "xkcd_"
    comics_num = 353
    
    response = requests.get(f"https://xkcd.com/{comics_num}/info.0.json")
    response.raise_for_status()
    comics_with_metadata = response.json()

    comics_alt = comics_with_metadata["alt"]
    comics_url = comics_with_metadata["img"]
    download_comics(comics_url, comics_folder_path, f"{comics_name_template}{comics_num}.png")


def main():
    env = Env()
    env.read_env()
    try:
        fetch_comics_and_metadata()
    except requests.exceptions.RequestException as error:
        print('Request error:\n', error.response)
        print('Request error text:\n', error.response.text)    

if __name__ == '__main__':
    main()
