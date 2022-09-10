from pathlib import Path
from pprint import pprint
import requests
from environs import Env
from functions import download_comics


def get_comics_from_xkcd() -> tuple([Path, str]):
    comics_folder_path = "files"
    comics_name_template = "xkcd"
    comics_num = 353
    
    response = requests.get(f"https://xkcd.com/{comics_num}/info.0.json")
    response.raise_for_status()
    comics_with_metadata = response.json()

    comics_url = comics_with_metadata["img"]
    comics_alt = comics_with_metadata["alt"]
    comics_file = download_comics(comics_url, comics_folder_path, f"{comics_name_template}.png")
    return comics_file, comics_alt

def get_vk_wall_upload_server_url(vk_access_token: str, vk_group_id: int, vk_api_version: str) -> str:
    params = {
        "access_token": vk_access_token,
        "group_id": vk_group_id,
        "v": vk_api_version,
    }
    response = requests.get(f"https://api.vk.com/method/photos.getWallUploadServer", params=params)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_photo_to_vk_server(vk_upload_server_url: str, comics_file: Path) -> dict:
    with open(comics_file, "rb") as file:
        files = {
            "photo": file
        }
        response = requests.post(vk_upload_server_url, files=files)
        response.raise_for_status()
    return response.json()


def save_photo_in_vk_group_album(vk_access_token: str, vk_group_id: int, vk_api_version: str, vk_photo_upload_info: dict) -> dict:
    params = {
        "access_token": vk_access_token,
        "group_id": vk_group_id,
        "photo": vk_photo_upload_info["photo"],
        "server": vk_photo_upload_info["server"],
        "hash": vk_photo_upload_info["hash"],
        "v": vk_api_version,
    }
    response = requests.post("https://api.vk.com/method/photos.saveWallPhoto", params=params)
    response.raise_for_status()
    return response.json()


def post_photo_on_vk_group_wall(vk_access_token: str, vk_group_id: int, vk_api_version: str, vk_photo_saving_info: dict, comics_description: str) -> None:
    params = {
        "access_token": vk_access_token,
        "owner_id": -vk_group_id,
        "from_group": 1,
        "attachments": f'photo{vk_photo_saving_info["response"][0]["owner_id"]}_{vk_photo_saving_info["response"][0]["id"]}',
        "message": comics_description,
        "v": vk_api_version,
    }
    response = requests.post("https://api.vk.com/method/wall.post", params=params)
    response.raise_for_status()


def publish_comics_to_vk(vk_access_token: str, vk_group_id: int, comics_file: Path, comics_description: str) -> None:
    vk_api_version = "5.131"
    vk_upload_server_url = get_vk_wall_upload_server_url(vk_access_token, vk_group_id, vk_api_version)
    vk_photo_upload_info = upload_photo_to_vk_server(vk_upload_server_url, comics_file)
    vk_photo_saving_info = save_photo_in_vk_group_album(vk_access_token, vk_group_id, vk_api_version, vk_photo_upload_info)
    post_photo_on_vk_group_wall(vk_access_token, vk_group_id, vk_api_version, vk_photo_saving_info, comics_description)


def main():
    env = Env()
    env.read_env()
    
    vk_access_token = env("VK_ACCESS_TOKEN")
    vk_group_id = env.int("VK_GROUP_ID")

    comics_folder_path = "files"
    comics_name_template = "xkcd.png"
    
    try:
        comics_file, comics_description = get_comics_from_xkcd()
        publish_comics_to_vk(vk_access_token, vk_group_id, comics_file, comics_description)
    except requests.exceptions.RequestException as error:
        print('Request error:\n', error.response)
        print('Request error text:\n', error.response.text)    

if __name__ == '__main__':
    main()
