import os
import time
import urllib
import datetime
import statistics as stats

# import pandas as pd
import feedparser as fp

from pathlib import Path


# def rss2df(rss: fp.util.FeedParserDict):
#     df_list = []
#     if rss is None:
#         return None

#     for entry in rss["entries"]:
#         entry_dict = {
#             "episode": entry["title"],
#             "link": entry["link"],
#             "published": time.strftime("%Y-%m-%d %H:%M:%S", entry["published_parsed"]),
#         }
#         df_list.append(entry_dict)
#     df = pd.DataFrame(df_list)
#     df["name"] = rss["feed"]["title"]
#     return df


def read_rss(url: str) -> fp.util.FeedParserDict:
    """
    Read the RSS feed from the given url.

    Parameters
    ----------
    url : str

    Returns
    -------
    fp.util.FeedParserDict
    """
    if not url:
        return None

    try:
        d = fp.parse(url)
    except urllib.error.URLError as e:
        print("urllib.error.URLError", e.reason)
        return None
    except OSError as e:
        print("OSError", e.reason)
        return None
    return d


def yaml2dict(filepath: Path) -> dict:
    """
    Read YAML front matter and convert it into a dict.

    Parameters
    ----------
    filepath : Path
        Path to the file with yaml front matter.

    Returns
    -------
    dict
        Dict made from the YAML front matter.
    """
    yaml_dict = {}
    with open(pod_f, "r") as f:
        lines = [i.strip() for i in f.readlines() if i.strip()][1:-1]

    for line in lines:
        line_split = line.split(":", 1)
        yaml_dict[line_split[0].strip()] = line_split[1].strip()

    return yaml_dict


def dict2yaml(yaml_dict: dict) -> str:
    """
    Convert the YAML dict into the YAML front matter string.

    Parameters
    ----------
    yaml_dict : dict
        Dict made from the YAML front matter.

    Returns
    -------
    str
        YAML front matter into string.
    """
    yaml_text = "---\n"
    for i in yaml_dict:
        line = f"{i}: {yaml_dict[i]}"
        yaml_text += f"{line.strip()}\n"
    yaml_text += "---\n"
    return yaml_text


def get_last_published(rss: fp.util.FeedParserDict) -> str:
    """
    Get the date of the most recently publised podcast episode.

    Parameters
    ----------
    rss : fp.util.FeedParserDict
        RSS feed of the podcast.

    Returns
    -------
    str
        Date in the "%Y-%m-%d %H:%M:%S" format.
    """
    if rss is None:
        return ""

    if rss["entries"]:
        dt = rss["entries"][0]["published_parsed"]
    elif "updated_parsed" in rss["feed"]:
        dt = rss["feed"]["updated_parsed"]
    dt = time.strftime("%Y-%m-%d %H:%M:%S", dt)
    return dt


def get_frequency(rss: fp.util.FeedParserDict) -> int or None:
    """
    Calculate the average time gap between episodes.

    Parameters
    ----------
    rss : fp.util.FeedParserDict
        RSS feed of the podcast.

    Returns
    -------
    int or None
    """

    if rss is None or not rss["entries"]:
        return None

    t1 = rss["entries"][0]["published_parsed"]
    t2 = rss["entries"][-1]["published_parsed"]
    time_window = time.mktime(t1) - time.mktime(t2)

    episodes = len(rss["entries"])
    freq = time_window / episodes
    freq = freq / (60 * 60 * 24)
    return int(round(freq))


def time2human(t: datetime.timedelta) -> str:
    """
    Convert timedelta into a human readable time string.

    Turn "01:35:00" time delta into "1 hours and 35 minutes".

    Parameters
    ----------
    t : datetime.timedelta

    Returns
    -------
    str
    """
    t_str = str(t)
    t_str = t_str.split(".")[0]
    hours = int(t_str.split(":")[0])
    minutes = int(t_str.split(":")[1])
    seconds = int(t_str.split(":")[2])

    if seconds > 40:
        minutes += 1

    t_human = ""
    if minutes:
        t_human = f"{minutes} mins"

    if hours == 1:
        t_human = f"1 hour {t_human}"
    elif hours > 1:
        t_human = f"{hours} hours {t_human}"

    return t_human


def get_avg_duration(rss: fp.util.FeedParserDict) -> str or None:
    """
    Calculate the average duration of episodes in the podcast.

    Calculate the average duration, then return time (mean - stddev) and
    (mean + stddev) as the lower and upper values of the duration respectively.

    Parameters
    ----------
    rss : fp.util.FeedParserDict
        RSS feed of the podcast.

    Returns
    -------
    str
        String in the format of "<lower limit> to <upper limit>".
    """
    if rss is None:
        return None

    durs = []
    for entry in rss["entries"]:
        # print(entry.keys())
        # print(entry)
        if "itunes_duration" not in entry:
            continue

        t_str = entry["itunes_duration"]
        t_list = [int(i) for i in t_str.split(":")]

        if len(t_list) == 1:
            t = datetime.timedelta(seconds=t_list[0])
        elif len(t_list) == 2:
            t = datetime.timedelta(minutes=t_list[0], seconds=t_list[1])
        elif len(t_list) == 3:
            t = datetime.timedelta(
                hours=t_list[0], minutes=t_list[1], seconds=t_list[2]
            )
        durs.append(t.seconds)

    if not durs:
        return None

    mean = datetime.timedelta(seconds=stats.mean(durs))
    std = datetime.timedelta(seconds=stats.stdev(durs))
    start = mean - std
    end = mean + std
    return f"{time2human(start)} to {time2human(end)}"


def get_podcast_activity(rss: fp.util.FeedParserDict) -> str:
    """
    Determine if the podcast is active or inactive.

    Calculate the number of days since the most recent episode date. If the
    ratio of number of days to the average gap between episodes is greater
    than 3, then it's marked as inactive, otherwise, it's considered active.

    Parameters
    ----------
    rss : fp.util.FeedParserDict
        RSS feed of the podcast.

    Returns
    -------
    str
        Returns "inactive" or "active"
    """
    if rss is None or not rss["entries"]:
        return ""

    today = time.gmtime()
    pod_recent = rss["entries"][0]["published_parsed"]
    diff = (time.mktime(today) - time.mktime(pod_recent)) / (60 * 60 * 24)
    freq = get_frequency(rss)

    diff2freq = diff / freq
    # print(diff2freq)
    if diff2freq <= 5:
        return "active"
    else:
        return "inactive"


def update_pod_details(rss: fp.util.FeedParserDict, pod_dets: dict) -> dict:
    """
    Update the details of the podcast from the RSS feed.

    Parameters
    ----------
    rss : : fp.util.FeedParserDict
        RSS feed of the podcast.
    pod_dets : dict
        Podcast details dict created from the YAML front matter

    Returns
    -------
    dict
        Updated podcast dict.
    """
    if rss is None:
        return pod_dets

    last_pub = get_last_published(rss)
    if last_pub:
        pod_dets["last_published"] = last_pub

    freq = get_frequency(rss)
    if freq:
        pod_dets["frequency"] = freq

    duration = get_avg_duration(rss)
    if duration:
        pod_dets["duration"] = duration

    activity = get_podcast_activity(rss)
    if activity:
        pod_dets["status"] = activity

    return pod_dets


def write_yaml(filepath: Path, yaml: str) -> None:
    """
    Write the YAML front matter string to the provided file.

    Parameters
    ----------
    filepath : Path
    yaml : str
        YAML front matter string
    """
    with open(filepath, "w") as f:
        f.write(yaml)


if __name__ == "__main__":
    posts_dir = Path("_posts")

    # dfs = []

    for pod_f in posts_dir.iterdir():
        print(pod_f)

        pod_dets = yaml2dict(pod_f)
        # print(pod_dets)

        rss = read_rss(pod_dets["rss"])

        pod_dets = update_pod_details(rss, pod_dets)

        yaml_text = dict2yaml(pod_dets)
        print(yaml_text)

        write_yaml(pod_f, yaml_text)

        # df = rss2df(rss)
        # dfs.append(df)

    # dfs = pd.concat(dfs)
    # dfs.to_csv("podcasts.csv", index=False)
