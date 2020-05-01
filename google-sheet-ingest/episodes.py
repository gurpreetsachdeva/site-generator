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
        self.youtube_embed_url = self.embed_youtube_video(self.youtube_id)

    def embed_youtube_video(self, embed_id):
        return 'https://youtube.com/embed/%s' % embed_id
