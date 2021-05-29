import sys
import datetime

from pathlib import Path


pod_name = sys.argv[1] if len(sys.argv) > 1 else "temp"
template = f"""---
layout: post
title: "{pod_name}"
categories: []
image: assets/images/pods/{pod_name}.webp
description: ""
podurl:
lang:
rss:
pocketcasts:
spotify:
apple_pod:
overcast:
youtube:
stitcher:
soundcloud:
last_published:
frequency:
duration:
status:
---
"""
print(template)


today = datetime.datetime.today().strftime("%Y-%m-%d")
file_name = f"{today}-{pod_name}.md"
file_path = Path("_posts") / file_name
with open(file_path, "w") as f:
    f.write(template)
print("Created empty podcast file-", file_path)
