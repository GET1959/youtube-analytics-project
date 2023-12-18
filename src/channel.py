import json
import os
from typing import Any

from dotenv import load_dotenv
from googleapiclient.discovery import build


load_dotenv()


class Channel:
    """
    Класс для ютуб-канала
    """

    api_key: str | None = os.getenv("API_YOUTUBE_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.channel_id = channel_id
        self.channel = (
            self.youtube.channels().list(id=channel_id, part="snippet,statistics").execute()
        )
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/" + self.channel_id
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, other: Any) -> int:
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other: Any) -> int:
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other: Any) -> bool:
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other: Any) -> bool:
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other: Any) -> bool:
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other: Any) -> bool:
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Channel):
            return self.subscriber_count == other.subscriber_count
        else:
            raise TypeError

    @classmethod
    def get_service(cls) -> Any:
        """
        Возвращает объект для работы с YouTube API.
        """
        api_key: str | None = os.getenv("API_YOUTUBE_KEY")
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube

    def to_json(self, file: str) -> None:
        """
        Сохраняет в файл значения атрибутов экземпляра Channel.
        """
        attr_dict = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count,
        }
        with open(file, "w", encoding="utf-8") as fp:
            json.dump(attr_dict, fp, ensure_ascii=False, indent=4)

        return None

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале.
        """
        info_json = json.dumps(self.channel, ensure_ascii=False, indent=2)
        print(info_json)
