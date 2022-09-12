from pathlib import Path
import requests


def download_comics(comics_url: str, file_path: str, filename: str) -> Path:
    Path(file_path).mkdir(parents=True, exist_ok=True)
    response = requests.get(comics_url)
    response.raise_for_status()
    
    filepath = Path(file_path, filename)
    with open(filepath, "wb") as file:
        file.write(response.content)
    return filepath
