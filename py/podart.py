import requests

from pathlib import Path
from bs4 import BeautifulSoup


def fetch_url(url: str) -> requests.models.Response:
    """
    Fetch the url using requests.

    Parameters
    ----------
    url : str

    Returns
    -------
    requests.models.Response
        Requests Response object for the `url`.
    """
    res = requests.get(url)
    return res


def download_img(img_url: str) -> requests.models.Response:
    """
    Download the image data from `img_url`.

    Parameters
    ----------
    img_url : str

    Returns
    -------
    requests.models.Response
        Requests Response object for the `url`.
    """
    return fetch_url(img_url)


def get_art_url(apple_pod_url: str) -> str:
    """
    Fetch the webp image link from the Apple podcast page.

    Parameters
    ----------
    apple_pod_url : str

    Returns
    -------
    str
    """
    html = fetch_url(apple_pod_url)
    soup = BeautifulSoup(html.text, "html.parser")

    art_url = (
        soup.find("source", class_="we-artwork__source")
        .attrs["srcset"]
        .split(",")[1]
        .split()[0]
    )
    return art_url


def tinypng_compress(img_url: str) -> bytes:
    """
    Fetch the original webp image and compress it using tinypng.

    Parameters
    ----------
    img_url : str

    Returns
    -------
    bytes
        Binary data of the compressed image.
    """
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

    # fetch the input image
    in_img = download_img(img_url)
    data = in_img.content

    # post request to compress the img
    res = requests.post("https://tinypng.com/web/shrink", headers=headers, data=data)

    # get the compressed img
    out_img_url = res.json()["output"]["url"]
    out_img = fetch_url(out_img_url)
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
