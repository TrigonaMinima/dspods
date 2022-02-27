import requests

from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup


def get_art_url(apple_pod_url: str) -> Optional[str]:
    """
    Fetch the webp image link from the Apple podcast page.

    Parameters
    ----------
    apple_pod_url : str

    Returns
    -------
    str or None
    """
    if not apple_pod_url or apple_pod_url is None:
        return None

    html = requests.get(apple_pod_url)

    art_url = None
    if html.status_code != 404:
        soup = BeautifulSoup(html.text, "html.parser")
        soup = soup.find("source", class_="we-artwork__source")
        if soup is not None:
            art_url = soup.attrs["srcset"].split(",")[1].split()[0]
    return art_url


def tinypng_compress(img_url: str) -> Optional[bytes]:
    """
    Fetch the original webp image and compress it using tinypng.

    Parameters
    ----------
    img_url : str

    Returns
    -------
    bytes or None
        Binary data of the compressed image.
    """
    if img_url is None or not img_url:
        return None

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "image/webp",
        "Origin": "https://tinypng.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://tinypng.com/",
        "TE": "Trailers",
    }

    # download the input image
    in_img = requests.get(img_url)
    data = in_img.content

    # post request to compress the img
    res = requests.post("https://tinypng.com/web/shrink", headers=headers, data=data)

    # download the compressed img
    out_img_url = res.json()["output"]["url"]
    out_img = requests.get(out_img_url)
    return out_img.content


def save_img(img: bytes, path: Path) -> None:
    """
    Save the binary image to the given path.

    Parameters
    ----------
    img : bytes
        Binary data of the compressed image.
    path : Path
    """
    with open(path, "wb") as f:
        f.write(img)
