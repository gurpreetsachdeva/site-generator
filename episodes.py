import datetime


class Episode(object):
    '''
    Describes a single episode of A Bootiful Podcast.
    '''

    def __init__(self,
                 title: str,
                 season_no: int,
                 blog_url: str,
                 date: datetime.datetime,
                 youtube_id: str):
        self.title = title
        self.seasonNo = season_no
        self.blog_url = blog_url
        self.date = date
        self.youtube_id = youtube_id


def embed_youtube_video(embed_id):
    return '''<iframe width="560" height="315" src="%s" frameborder="0" allowfullscreen></iframe>'''.strip() % embed_id
