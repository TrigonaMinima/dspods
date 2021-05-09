import feedparser as fp

from pathlib import Path

from py.yamlproc import yaml2dict, dict2yaml, write_yaml
from py.rssproc import (
    read_rss,
    get_last_published,
    get_frequency,
    get_avg_duration,
    get_podcast_activity,
)


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
