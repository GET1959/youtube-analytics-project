import os
from datetime import timedelta
import isodate
from typing import Any

from dotenv import load_dotenv
from googleapiclient.discovery import build
from src.video import get_info

load_dotenv()


PLAYLIST_ID = "PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"
CHANNEL_ID = "UC-OVMPlMA3-YCIeg4z5z23A"


def get_playlist(playlist_id: str = PLAYLIST_ID, channel_id: str = CHANNEL_ID) -> Any:
    """
    Функция принимает на вход playlist_id, channel_id и возвращает статистику по плейлисту.
    """
    api_key: str = os.getenv("API_YOUTUBE_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)
    playlists = (
        youtube.playlists()
        .list(
            channelId=channel_id,
            part="contentDetails,snippet",
            maxResults=50,
        )
        .execute()
    )
    for playlist in playlists["items"]:
        if playlist["id"] == playlist_id:
            return playlist


class PlayList:
    def __init__(self, playlist_id: str):
        self.playlist_info = get_info(playlist_id=playlist_id)
        self.title = get_playlist(playlist_id)["snippet"]["title"]
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id

    @property
    def total_duration(self) -> timedelta:
        playlist_durations = [
            isodate.parse_duration(
                get_info(item["contentDetails"]["videoId"])["items"][0]["contentDetails"]["duration"]
            )
            for item in self.playlist_info["items"]
        ]
        total_dur = timedelta()
        for dur in playlist_durations:
            total_dur += dur

        return total_dur

    def show_best_video(self):
        videos = {
            "https://youtu.be/"
            + get_info(item["contentDetails"]["videoId"])["items"][0]["id"]: int(
                get_info(item["contentDetails"]["videoId"])["items"][0]["statistics"]["likeCount"]
            )
            for item in self.playlist_info["items"]
        }
        best_video = max(videos, key=videos.get)

        return best_video
