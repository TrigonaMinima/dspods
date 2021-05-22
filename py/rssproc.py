import time
import urllib
import datetime
import statistics as stats

import feedparser as fp

from urllib import error


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
    except error.URLError as e:
        print("urllib.error.URLError", e.reason)
        return None
    except OSError as e:
        print(f"OSError: Code - {e.errno}, Message: {e.strerror}")
        return None
    return d


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
    dt = ""
    if rss is None:
        return dt

    if rss["entries"]:
        dt = rss["entries"][0]["published_parsed"]
    elif "updated_parsed" in rss["feed"]:
        dt = rss["feed"]["updated_parsed"]

    if dt:
        dt = time.strftime("%Y-%m-%d %H:%M:%S", dt)
    return dt


def get_frequency(rss: fp.util.FeedParserDict) -> int:
    """
    Calculate the average time gap between episodes.

    Parameters
    ----------
    rss : fp.util.FeedParserDict
        RSS feed of the podcast.

    Returns
    -------
    int
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


def get_avg_duration(rss: fp.util.FeedParserDict) -> str:
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
    if freq > 30:
        if diff2freq <= 3:
            return "active"
        else:
            return "inactive"
    elif diff2freq <= 5:
        return "active"
    else:
        return "inactive"


def rss2json(rss: fp.util.FeedParserDict):
    json_list = []
    if rss is None:
        return None

    dt_format = "%Y-%m-%d %H:%M:%S"

    for entry in rss["entries"]:
        entry_dict = {
            "epi_title": entry["title"],
            "epi_pub_date": time.strftime(dt_format, entry["published_parsed"]),
            "epi_summary": entry["summary"],
            "epi_summary_big": entry.get("content", [{"value": ""}])[0]["value"],
            "epi_duration": entry.get("itunes_duration", 0),
        }
        json_list.append(entry_dict)
    return json_list


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
