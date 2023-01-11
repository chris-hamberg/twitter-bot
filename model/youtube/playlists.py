try:
    from model.youtube.youtube import Youtube
except ModuleNotFoundError:
    from youtube import Youtube
import googleapiclient.discovery
import logging
import random


log = logging.getLogger(__name__)


class YoutubePlaylists(Youtube):


    def __init__(self, admin, emojis = None, p = None):
        super().__init__(admin, emojis, p)
        self.youtube = googleapiclient.discovery.build(
                "youtube", "v3", developerKey = admin.youtube_api)
        self.stem = "https://www.youtube.com/watch?v={id}"
        self.type = "playlist"


    def get(self, playlist_id):
        playlist, count = [], 0
        request  = self.youtube.playlistItems().list(
                part = "snippet",
                playlistId = playlist_id,
                maxResults = 50)
        while request is not None:
            response = request.execute()
            for video in response["items"]:
                video = self.parse(video, playlist_id)
                if not video:
                    continue
                playlist.append(video)
            self.admin.orm.api.youtube.create(playlist)
            count += len(playlist)
            playlist.clear()
            request = self.youtube.playlistItems().list_next(request, response)
        message = f"Downloaded {count} videos for playlist: {playlist_id}"
        self.admin.orm.api.messages.create(message, "youtube")
        log.debug(f"{self.admin.name}\n{message}")


    def parse(self, video, playlist_id):
        title = video["snippet"]["title"]
        if (title == "Private video"):
            return False
        return (self.type,
                self.admin.id,
                video["snippet"]["channelId"],
                playlist_id,
                video["snippet"]["resourceId"]["videoId"],
                title,
                self.stem.format(id = 
                    video["snippet"]["resourceId"]["videoId"]),
                self.emojis,
                str(),
                False)
