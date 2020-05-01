import pickle
import os.path
import re

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import json


def obtain_token(credentials_config_str: str) -> Credentials:
    '''
        If modifying these scopes, delete the file token.pickle.
    '''
    scopes = ['https://www.googleapis.com/auth/drive']
    credentials: Credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(credentials_config_str, scopes)
            credentials = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)
    return credentials


class GSheet(object):
    USER_ENTERED = 'USER_ENTERED'
    INPUT_VALUE_OPTION_UNSPECIFIED = 'INPUT_VALUE_OPTION_UNSPECIFIED'
    RAW = 'RAW'

    def write_values(self, spreadsheet_range: str, input_option: str, values: list):
        write_spreadsheet_values(self.service, self.id, spreadsheet_range, input_option, values)

    def read_values(self, spreadsheet_range: str) -> list:
        return read_spreadsheet_values(self.service, self.id, spreadsheet_range)

    def __init__(self, credentials: str, spreadsheet_id):
        token = obtain_token(credentials)
        self.service = build('sheets', 'v4', credentials=token)
        self.id = spreadsheet_id


def read_spreadsheet_values(service, sample_spreadsheet_id, sample_range_name) -> list:
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=sample_spreadsheet_id, range=sample_range_name).execute()
    return result.get('values', [])


def write_spreadsheet_values(service, spreadsheet_id, range_name, value_input_option, values):
    body = {'values': values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))
    return result


def main():
    sample_spreadsheet_id = '13EoEqvqr3dR4eVW6twNTooxBl3ayNhlyKO7ip0zykKE'
    with open('credentials.json', 'r') as json_file:
        client_config = json.load(json_file)
    sheet = GSheet(client_config, sample_spreadsheet_id)
    values = sheet.read_values('Published!A1:E')
    ctr = 0
    for title, season, blog_url, date, youtube_id in values:
        print('-' * 100)
        print('title:', title)
        print('season:', season)
        print('blog_url:', blog_url)
        print('date:', date)
        print('youtube_id:', date)
        # yt_video_id = find_youtube_video_from_blog_page(blog_url)
        # ctr += 1
        # cell = 'E%s' % ctr
        # sheet.write_values(cell, GSheet.USER_ENTERED, [[yt_video_id]])


def find_youtube_video_from_blog_page(http_url: str) -> str:
    '''
    This function surmises that, all things being equal, the most likely embed ID for
    the YouTube video is the embed ID that occurs most commonly on a given blog page.

    :param http_url: the spring.io/blog page
    :return: the embed_id corresponding to the youtube video for the topic on the blog page.
    '''

    page = requests.get(http_url)
    html = str(page.content)
    embed_re = re.compile(r'youtube.com/embed/(.*)("|&quot;)')
    results = [a[0].split('&quot;')[0] for a in embed_re.findall(html)]
    embed_ids_to_frequency = {}
    for r in results:
        embed_ids_to_frequency[r] = embed_ids_to_frequency.get(r, 0) + 1
    max_frequency: int = max([k[1] for k in embed_ids_to_frequency.items()])
    embed_id = \
        [(embed, frequency) for embed, frequency in embed_ids_to_frequency.items() if frequency == max_frequency][0][0]
    return embed_id


def embed_youtube_video(embed_id):
    return ''' <iframe width="560" height="315" src="%s" frameborder="0" allowfullscreen></iframe>'''.strip() % embed_id


if __name__ == '__main__':
    main()
