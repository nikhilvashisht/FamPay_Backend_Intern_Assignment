from googleapiclient.discovery import build
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from . import models
import threading
import asyncio


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_datetime(date_time):
    """
        Returns a DateTime object from a string

        Arguments : 
            a string in "YYYYmmddTHHMMSSZ" format
        
        Return :
            A DateTime object which can be saved in db
    """
    date_time_data = date_time.split(
        'T')[0] + ' ' + date_time.split('T')[1].split('Z')[0]
    date_time_format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(date_time_data, date_time_format)


def get_video_data(response):
    """
        Returns a dictionary of video data from json response
        which can be directly saved in db

        Arguments : 
            json response of a single video
        
        Returns:
            dictionary having video fields 
            {video_id, published_datetime, video_title, description, channel_title}
    """
    if 'videoId' in response['id']:
        video_id = response['id']['videoId']
    else:
        video_id = ''
    return {
        'video_id': video_id,
        'published_datetime': get_datetime(response["snippet"]["publishedAt"]),
        'video_title': response["snippet"]["title"],
        'description': response["snippet"]["description"],
        'channel_title': response["snippet"]["channelTitle"]
    }


def get_thumbnail_data(response):
    """
        Similar to get_video_data, returns a dictionary of thumbnail data from json response
        which can be directly saved in db

        Arguments : 
            json response of a single video
        
        Returns:
            dictionary having video thumbnail fields 
            {thumbnail_type, url}
    """
    return [
        {
            'thumbnail_type': thumbnail_type,
            'url': response["snippet"]["thumbnails"][thumbnail_type]["url"]
        } for thumbnail_type in response["snippet"]["thumbnails"]
    ]


def save_data_to_db(items):
    """
        Saves video to db

        Arguments:
            json response from YouTube API
    """
    for item in items:
        video_data = get_video_data(item)
        thumbnail_data = get_thumbnail_data(item)

        video_object = models.Video(**video_data)
        video_object.save()

        for thumbnail in thumbnail_data:
            thumbnail['video'] = video_object
            thumbnail_object = models.VideoThumbnail(**thumbnail)
            thumbnail_object.save()


def yt_search():
    """
        Performs search on youtube on a predefined query (football) \n
        The DEVELOPER_KEY is taken from db. Incase the key is exhausted, 
        a new key is taken from db automatically.

    """
    #fetch non-exhausted keys
    api_keys = models.APIKeys.objects.filter(exhausted=False)

    #we take the first key out of non-exhausted keys
    api_key = api_keys[0].key

    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME,
                        YOUTUBE_API_VERSION,
                        developerKey=api_key)
        search_response = youtube.search().list(
            q="football",
            maxResults=25,
            part="id, snippet"
        ).execute()

        search_results = search_response["items"]
        return search_results
    except:
        #this means the current key being used is exhausted
        #mark the key as exhausted and save to update its value
        api_key[0].exhausted = True
        api_key[0].save()
        return []


def search_and_add_items():
    """
        A helper function which runs the search and saves data to db.
    """
    items = yt_search()
    save_data_to_db(items)


def service():
    """
        Main function which runs in background
    """
    while True:
        asyncio.run(search_and_add_items())
        asyncio.sleep(10)


THREAD = threading.Thread(target=service)
