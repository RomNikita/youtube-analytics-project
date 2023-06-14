import os
import json
from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        for i in channel["items"]:
            self.title = i["snippet"]["title"]
            self.video_count = i["statistics"]["videoCount"]
            self.description = i["snippet"]["description"]
            self.subs = i["statistics"]["subscriberCount"]
            self.views_count = i["statistics"]["viewCount"]

    @property
    def print_title(self):
        return self.title

    @property
    def print_video_count(self):
        return self.video_count

    @property
    def print_description(self):
        return self.description

    @property
    def print_subs(self):
        return self.subs

    @property
    def print_views_count(self):
        return self.video_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        printj(channel)

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename):
        with open(filename, 'w', encoding='UTF-8') as file:
            channel_items = {"id": self.__channel_id,
                             "title": self.title,
                             "desription": self.description,
                             "url": self.url,
                             "subs": self.subs,
                             "videos_count": self.video_count,
                             "views_count": self.views_count}
            json.dump(channel_items, file, ensure_ascii=False)

    def __str__(self):
        """магический str метод"""
        return f"{self.title} ({self.url})"


    def __add__(self, other):
        """Метод срабатывает, когда используется оператор сложения.
	    В параметре other хранится то, что справа от знака +"""

        return int(self.subs) + int(other.subs)

    def __sub__(self, other):
        """Метод срабатывает, когда используется оператор вычитания"""
        return int(self.subs) - int(other.subs)

    def __lt__(self, other):
        return int(self.subs) < int(other.subs)

    def __le__(self, other):
        return int(self.subs) <= int(other.subs)

    def __gt__(self, other):
        return int(self.subs) > int(other.subs)

    def __ge__(self, other):
        return int(self.subs) >= int(other.subs)