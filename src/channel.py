import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_YOUTUBE_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        info_json = json.dumps(self.channel, ensure_ascii=False, indent=2)
        print(info_json)
