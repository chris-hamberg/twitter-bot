from model.M.engage.tweets.objects.super import SuperTweetObject
from model.M.content.interface import YouTubeManager


class Playlist(SuperTweetObject):


    def __init__(self, admin): 
        super().__init__(admin)
        self.youtube = YouTubeManager(admin)


    def execute(self):
        self.youtube.refresh_playlists("playlist")
        tweet, video = self.preprocessor.get("playlist")
        _ = self._subexecution_type1(tweet)
        r = self._subexecution_type2("playlist")
        self._terminate(r, video)
        return r, tweet


    def _terminate(self, r, video):
        super()._terminate(r)
        self.admin.orm.api.youtube.update(video[4])
        self.admin.orm.api.state.tweetAI_injection_state = False
