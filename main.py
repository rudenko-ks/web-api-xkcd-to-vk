from pathlib import Path
import random
import requests
from environs import Env
from functions import download_comic


def get_comic_from_xkcd() -> tuple[Path, str]:
    comic_folder_path = "files"
    comic_name_template = "xkcd"

    last_comic = requests.get("https://xkcd.com/info.0.json")
    last_comic.raise_for_status()

    last_comic_num = last_comic.json()["num"]
    random_comic = random.randint(0, last_comic_num)
    response = requests.get(f"https://xkcd.com/{random_comic}/info.0.json")
    response.raise_for_status()
    comic_with_metadata = response.json()

    comic_url = comic_with_metadata["img"]
    comic_alt = comic_with_metadata["alt"]
    comic_filepath = download_comic(comic_url, comic_folder_path, f"{comic_name_template}.png")
    return comic_filepath, comic_alt


def get_vk_wall_upload_server_url(vk_access_token: str, vk_group_id: int, vk_api_version: str) -> str:
    params = {
        "access_token": vk_access_token,
        "group_id": vk_group_id,
        "v": vk_api_version,
    }
    response = requests.get(f"https://api.vk.com/method/photos.getWallUploadServer", params=params)
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_photo_to_vk_server(vk_upload_server_url: str, comic_filepath: Path) -> dict:
    with open(comic_filepath, "rb") as file:
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


def post_photo_on_vk_group_wall(vk_access_token: str, vk_group_id: int, vk_api_version: str, vk_photo_saving_info: dict, comic_description: str) -> None:
    params = {
        "access_token": vk_access_token,
        "owner_id": -vk_group_id,
        "from_group": 1,
        "attachments": f'photo{vk_photo_saving_info["response"][0]["owner_id"]}_{vk_photo_saving_info["response"][0]["id"]}',
        "message": comic_description,
        "v": vk_api_version,
    }
    response = requests.post("https://api.vk.com/method/wall.post", params=params)
    response.raise_for_status()


def publish_comic_to_vk(vk_access_token: str, vk_group_id: int, comic_filepath: Path, comic_description: str) -> None:
    vk_api_version = "5.131"
    vk_upload_server_url = get_vk_wall_upload_server_url(vk_access_token, vk_group_id, vk_api_version)
    vk_photo_upload_info = upload_photo_to_vk_server(vk_upload_server_url, comic_filepath)
    vk_photo_saving_info = save_photo_in_vk_group_album(vk_access_token, vk_group_id, vk_api_version, vk_photo_upload_info)
    post_photo_on_vk_group_wall(vk_access_token, vk_group_id, vk_api_version, vk_photo_saving_info, comic_description)


def main():
    env = Env()
    env.read_env()
    
    vk_access_token = env("VK_ACCESS_TOKEN")
    vk_group_id = env.int("VK_GROUP_ID")

    try:
        comic_filepath, comic_description = get_comic_from_xkcd()
        publish_comic_to_vk(vk_access_token, vk_group_id, comic_filepath, comic_description)
        comic_filepath.unlink()
    except requests.exceptions.RequestException as error:
        print('Request error:\n', error.response)
        print('Request error text:\n', error.response.text)    

if __name__ == '__main__':
    main()
