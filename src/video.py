from googleapiclient.discovery import build

api_key: str = 'AIzaSyBzMRf2HZvF7lB6zRbp6ZB6xMLuq9oPEsc'
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id).execute()

        self.url = f'https://www.youtube.com/watch?v={self.video_id}'

        for i in video_response['items']:
            self.title = i['snippet']['title']
            self.video_count = i['statistics']['viewCount']
            self.likes_count = i['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f'{self.title}'
