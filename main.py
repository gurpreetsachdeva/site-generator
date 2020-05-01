import datetime
import json
import typing

import PyRSS2Gen

import episodes
from sheets import *


def build_rss_item_for_episode(episode: episodes.Episode) -> PyRSS2Gen.RSSItem:
    return PyRSS2Gen.RSSItem(title=episode.title, link=episode.blog_url, description='', pubDate=episode.date)


def write_rss(fn: str, episodes: typing.List[episodes.Episode]) -> None:
    items: typing.List[PyRSS2Gen.RSSItem] = [build_rss_item_for_episode(e) for e in episodes]
    rss = PyRSS2Gen.RSS2(
        title="Spring Tips",
        link="http://bit.ly/spring-tips-playlist",
        description="Spring Tips is a YouTube playlist by Josh Long (@starbuxman) that "
                    "looks at different aspects of the wonderful and wide world of Springdom",
        lastBuildDate=datetime.datetime.now(),
        items=items
    )
    with open(fn, "w") as fp:
        rss.write_xml(fp)


def main(args):
    spreadsheet_id = '13EoEqvqr3dR4eVW6twNTooxBl3ayNhlyKO7ip0zykKE'
    with open('credentials.json', 'r') as json_file:
        client_config = json.load(json_file)
    sheet = GSheet(client_config, spreadsheet_id)
    values = sheet.read_values('Published!A1:E')
    episodes_list = []
    for title, season, blog_url, date, youtube_id in values:
        print('title:', title, 'season:', season, 'blog_url:', blog_url, 'date:', date, 'youtube_id:', youtube_id)
        m, d, y = [int(x) for x in date.split('/')]
        date = datetime.datetime(y, m, d)
        episode = episodes.Episode(title, int(season), blog_url, date, youtube_id)
        episodes_list.append(episode)

    if len(args) == 2:
        fn = args[0]
    else:
        fn = 'spring-tips.xml'
    write_rss(fn, episodes_list)


if __name__ == '__main__':
    import sys

    main(sys.argv)
