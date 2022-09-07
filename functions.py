import os.path
from pathlib import Path
import requests
import urllib.parse


def download_comics(comics_url: str, file_path: str, filename: str) -> None:
    Path(file_path).mkdir(parents=True, exist_ok=True)
    response = requests.get(comics_url)
    response.raise_for_status()
    
    file = Path(file_path, filename)
    with open(file, "wb") as file:
        file.write(response.content)
