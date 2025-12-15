from requests import Response
from bs4 import BeautifulSoup
import requests
from pathlib import Path
from yarl import URL

def find_image(response: Response):
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        
        main_div = soup.find("div", attrs={"class": "sc-1c12727-0 AKTGB media-viewer", "data-testid": "media-viewer"})
        
        image_div = main_div.find_next("div", {"class": "sc-b66608db-2 cEjYQy"})
        
        image = image_div.find_next("img")
        
        return image
    except Exception as error:
        raise RuntimeError(f"Error mientras se buscaba la imagen: {error}")
    
def download_img(alt: str, image_src: str, path: str) -> Path:
    try:
        full_path = f"{path}{alt}.{image_src.split(".")[-1]}"
        with open(full_path.replace(":", "_"), "wb") as image:
            image.write(requests.get(image_src).content)
        
        return Path(full_path)
        
    except Exception as error:
        raise RuntimeError(f"Error intentando descargar la imagen: {error}")
    
def fix_url(main_url: str, url_to_fix: str) -> str:
    return URL(f"{main_url}/{'/'.join(url_to_fix.split("/")[2:])}")