from datetime import timedelta

from googleapiclient.discovery import build

api_key: str = 'AIzaSyBzMRf2HZvF7lB6zRbp6ZB6xMLuq9oPEsc'
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.youtube = youtube
        playlist_info = self.youtube.playlists().list(part='snippet', id=playlist_id).execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

        self.videos = []
        next_page_token = None
        while True:
            playlist_items = self.youtube.playlistItems().list(part='snippet,contentDetails',
                                                               playlistId=self.playlist_id,
                                                               pageToken=next_page_token).execute()
            for item in playlist_items['items']:
                title = item['snippet']['title']
                duration = item['contentDetails'].get('duration', 'PT0S')
                likes = item['snippet']['resourceId']['videoId']
                link = f'https://www.youtube.com/watch?v={item["snippet"]["resourceId"]["videoId"]}'
                self.videos.append({'title': title, 'duration': duration, 'likes': likes, 'link': link})
            next_page_token = playlist_items.get('nextPageToken')
            if not next_page_token:
                break

    @property
    def total_duration(self):
        total = timedelta()
        for video in self.videos:
            duration = video['duration']
            duration = duration.replace('PT', '').replace('H', ':').replace('M', ':').replace('S', '')
            duration_list = []
            for x in duration.split(':'):
                duration_list.append(int(x))
            if len(duration_list) < 3:
                duration_list = [0] * (3 - len(duration_list)) + duration_list
            video_duration = timedelta(hours=duration_list[0], minutes=duration_list[1], seconds=duration_list[2])
            total += video_duration
        return total

    def show_best_video(self):
        best_video = max(self.videos, key=lambda x: x['likes'])
        return best_video['link']