from pathlib import Path
from pprint import pprint
import requests
from environs import Env
from functions import download_comics


def fetch_comics_and_metadata() -> None:
    comics_folder_path = "files"
    comics_name_template = "xkcd"
    comics_num = 353
    
    response = requests.get(f"https://xkcd.com/{comics_num}/info.0.json")
    response.raise_for_status()
    comics_with_metadata = response.json()

    comics_alt = comics_with_metadata["alt"]
    comics_url = comics_with_metadata["img"]
    download_comics(comics_url, comics_folder_path, f"{comics_name_template}.png")


def get_vk_wall_upload_server_url(vk_access_token: str, vk_group_id: int, vk_api_version: str) -> str:
    params = {
        "access_token": vk_access_token,
        "group_id": vk_group_id,
        "v": vk_api_version,
    }
    response = requests.get(f"https://api.vk.com/method/photos.getWallUploadServer", params=params)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_photo_to_vk_server(vk_upload_server_url: str) -> dict:
    file = Path("files", "xkcd_354.png")
    with open(file, "rb") as file:
        files = {
            "photo": file
        }
        response = requests.post(vk_upload_server_url, files=files)
        response.raise_for_status()
    return response.json()


def publish_comics_to_vk(vk_access_token: str, vk_group_id: int) -> None:
    vk_api_version = "5.131"
    vk_upload_server_url = get_vk_wall_upload_server_url(vk_access_token, vk_group_id, vk_api_version)
    vk_photo_upload_info = upload_photo_to_vk_server(vk_upload_server_url)


def main():
    env = Env()
    env.read_env()
    
    vk_access_token = env("VK_ACCESS_TOKEN")
    vk_group_id = env.int("VK_GROUP_ID")
    
    try:
        # fetch_comics_from_xkcd()
        publish_comics_to_vk(vk_access_token, vk_group_id)
    except requests.exceptions.RequestException as error:
        print('Request error:\n', error.response)
        print('Request error text:\n', error.response.text)    

if __name__ == '__main__':
    main()
