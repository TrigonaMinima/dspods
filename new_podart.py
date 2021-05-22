from pathlib import Path

from py.podart import get_art_url, tinypng_compress, save_img


if __name__ == "__main__":
    pod_url = "https://podcasts.apple.com/us/podcast/practical-ai/id1406537385"
    podart_url = get_art_url(pod_url)

    if podart_url is not None:
        podart = tinypng_compress(podart_url)

        img_name = "temp.webp"
        podart_path = Path(img_name)
        # podart_path = Path("assets/images/pods/") / img_name
        save_img(podart, podart_path)
        print("Saved the compressed image at:", podart_path)
    else:
        print("Page 404")
