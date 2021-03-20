import requests

from pathlib import Path
from bs4 import BeautifulSoup


def fetch_url(url):
    res = requests.get(url)
    return res


def get_art_url(apple_pod_url):
    html = fetch_url(apple_pod_url)
    soup = BeautifulSoup(html.text, "html.parser")

    art_url = (
        soup.find("source", class_="we-artwork__source")
        .attrs["srcset"]
        .split(",")[1]
        .split()[0]
    )
    return art_url


def download_img(img_url):
    return fetch_url(img_url)


def tinypng_compress(in_img_url):
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
    in_img = download_img(in_img_url)
    data = in_img.content

    # post request to compress the img
    res = requests.post("https://tinypng.com/web/shrink", headers=headers, data=data)

    # get the compressed img
    img_url = res.json()["output"]["url"]
    out_img = requests.get(img_url)
    return out_img.content


def save_img(img, path="a.webp"):
    with open(path, "wb") as f:
        f.write(img)


if __name__ == "__main__":
    img_name = "datatalks.club.webp"
    pod_url = "https://podcasts.apple.com/us/podcast/id1541710331"
    art_url = get_art_url(pod_url)
    img = tinypng_compress(art_url)

    img_path = Path("assets/images/pods/") / img_name
    save_img(img, img_path)
    print("Saved the compressed image at:", img_path)
