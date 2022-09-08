import os
import datetime
from pprint import pprint
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


def test_vk_api(vk_client_id: int, vk_access_token: str, vk_group_id: int, vk_album_id: int) -> None:
    api_version = 5.131
    params = {
        "access_token": vk_access_token,
        "v": api_version
    }

    response = requests.get(f"https://api.vk.com/method/groups.get", params=params)
    response.raise_for_status()
    vk_groups = response.json()
    pprint(vk_groups)


def main():
    env = Env()
    env.read_env()
    
    vk_client_id = env.int("VK_CLIENT_ID")
    vk_access_token = env("VK_ACCESS_TOKEN")
    vk_group_id = env.int("VK_GROUP_ID")
    vk_album_id = env.int("VK_ALBUM_ID")
    
    try:
        # fetch_comics_and_metadata()
        test_vk_api(vk_client_id, vk_access_token, vk_group_id, vk_album_id)
    except requests.exceptions.RequestException as error:
        print('Request error:\n', error.response)
        print('Request error text:\n', error.response.text)    

if __name__ == '__main__':
    main()
