import sys
from pathlib import Path

from py.yamlproc import yaml2dict
from py.podart import get_art_url, tinypng_compress, save_img


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"

    posts_dir = Path("_posts")
    if arg == "all":
        files_iter = posts_dir.iterdir()
    else:
        files_iter = posts_dir.glob(f"*{arg}*")

    for pod_f in files_iter:
        print(pod_f)

        pod_dets = yaml2dict(pod_f)
        # print(pod_dets)

        podart_path = Path(pod_dets["image"])
        podart_url = get_art_url(pod_dets["apple_pod"])

        if podart_url is not None:
            podart = tinypng_compress(podart_url)

            if podart is not None:
                save_img(podart, podart_path)
                print("Saved the compressed image at:", podart_path)
        else:
            print("Skipped fetching podart")
