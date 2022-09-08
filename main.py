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
        "v": api_version,
        "group_id": vk_group_id,
        "album_id": vk_album_id
    }
    response = requests.get(f"https://api.vk.com/method/photos.getWallUploadServer", params=params)
    response.raise_for_status()
    vk_upload_server_info = response.json()
    pprint(vk_upload_server_info)

    with open("files/xkcd_353.png", "rb") as file:
        files = {
            "photo": file
        }
        response = requests.post(vk_upload_server_info["response"]["upload_url"], files=files)
        response.raise_for_status()
    vk_comics_upload_info = response.json()
    pprint(vk_comics_upload_info)


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



# https://api.vk.com/method/groups.get?access_token=vk1.a.3S3uN0EzsNvG7-JpCEcmfxsSg85jNHnTmxIxFxaBgpUAZHodyKU4tL9uC9zJfe3dPeTdH6B3eysBoSyeuh4KXUZ9KLUaGvB7alVMtHKABU_ryQzjM650QTYKTpX5ISMD2lJ2XZe1MPMavm7LEdR05FBvN3HDGHXbXYCh3xLjUNfh1uJBjPP1HV5R9g1nNAT7&v=5.131

# {"response":{"count":33,"items":[90038880,33393308,53895352,94385733,61281696,168874636,16623569,63731512,36284347,58267631,166523849,41452622,14448489,45135634,140444023,10042064,117483992,29559271,59767730,45446503,4489985,34867792,54046061,43948962,41890491,75313533,47535457,44743077,64834463,13074721,2190892,15798779,215837914]}}


# https://api.vk.com/method/photos.getUploadServer?access_token=vk1.a.3S3uN0EzsNvG7-JpCEcmfxsSg85jNHnTmxIxFxaBgpUAZHodyKU4tL9uC9zJfe3dPeTdH6B3eysBoSyeuh4KXUZ9KLUaGvB7alVMtHKABU_ryQzjM650QTYKTpX5ISMD2lJ2XZe1MPMavm7LEdR05FBvN3HDGHXbXYCh3xLjUNfh1uJBjPP1HV5R9g1nNAT7&v=5.131&group_id=215837914&album_id=284992581

# {"response":{"album_id":284992581,"upload_url":"https:\/\/pu.vk.com\/c856312\/ss2152\/upload.php?act=do_add&mid=202050440&aid=284992581&gid=215837914&hash=9a5a7ac3681cab21e2ac1a048279700d&rhash=890c893440a19b4a7a803a0fcb286c78&swfupload=1&api=1","user_id":202050440}}