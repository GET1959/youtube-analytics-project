import os
from typing import Any

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


VIDEO_ID = "4fObz_qw9u4"


def get_info(video_id=None, playlist_id=None) -> Any:
    """
    Функция принимает на вход video_id и опционально playlist_id.
    Если playlist_id не передан, возвращает статистику по видео,
    если передаетя и video_id, и playlist_id, -  возвращает данные по плейлисту.
    """
    api_key: str = os.getenv("API_YOUTUBE_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)
    if playlist_id:
        return (
            youtube.playlistItems()
            .list(
                playlistId=playlist_id,
                part="contentDetails",
                maxResults=50,
            )
            .execute()
        )
    else:
        return youtube.videos().list(part="snippet,statistics,contentDetails", id=video_id).execute()


class Video:
    """
    Класс для получения статистики по видео.
    """

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_info = get_info(video_id)
        try:
            self.title = self.video_info["items"][0]["snippet"]["title"]
            self.view_count = self.video_info["items"][0]["statistics"]["viewCount"]
            self.like_count = self.video_info["items"][0]["statistics"]["likeCount"]
            self.video_url = "https://www.youtube.com/watch?v=" + self.video_id
        except IndexError:
            self.title = None
            self.viewCount = None
            self.like_count = None
            self.video_url = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    """
    Класс для получения статистики по видео и данных по плейлисту.
    """

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_info = get_info(video_id, playlist_id)

    def __str__(self):
        return self.title
