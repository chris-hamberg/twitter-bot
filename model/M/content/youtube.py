from model.objects.exceptions import RateLimitException
from model.youtube.playlists import YoutubePlaylists
from model.youtube.streamer import RSSStreamer
from model.objects.normalize import normalize
from datetime import timedelta
from datetime import datetime
import requests
import logging
import random
import time


log = logging.getLogger(__name__)


class YouTubeManager:


    def __init__(self, admin):
        self.admin = admin
        self.name  = "youtube"


    def execute(self):
        delta = normalize(self.admin.orm.api.state.playlist_delta)
        if ((not delta) or ((delta) and (delta <= datetime.utcnow()))):
            length = self._get_playlist()
            self._subcycle("playlist", length, 22, 26, 60, 120)
            return True
        try:
            length = self._get_stream()
            self._subcycle("ystream", length, 1, 3, 40, 90)
        except (IndexError, AssertionError):
            pass


    def refresh_playlists(self, type):
        if (type != "playlist"): return None
        videos  = self.admin.orm.api.youtube.read(type=type,posted=False)
        if len(videos): return None
        self.admin.orm.api.youtube.update(posted = False, type = type)


    def _subcycle(self, endpoint, length, m, n, p, q):
        index = getattr(self.admin.orm.api.state, f"{endpoint}_subcycle_index")
        if (length <= index): 
            index = 0
            n     = random.randint(m, n)
            delta = datetime.utcnow() + timedelta(hours = n)
        else: 
            index += 1
            n      = random.randint(p, q)
            delta  = datetime.utcnow() + timedelta(minutes = n)
        setattr(self.admin.orm.api.state, f"{endpoint}_subcycle_index", index)
        setattr(self.admin.orm.api.state, f"{endpoint}_delta", delta)


    def _get_playlist(self):
        playlists   = self.admin.orm.api.youtube.read(type="playlist", Xid=True)
        index       = self.admin.orm.api.state.playlist_index
        if not len(playlists):
            message = "No playlists found in database. Set configuration."
            self.admin.orm.api.messages.create(message, self.name)
            log.debug(f"{self.admin.name}\n{message}")
        try: playlist = playlists[index]
        except IndexError:
            self.admin.orm.api.state.playlist_index = index = 0
            playlist = playlists[index]
        playlist_id = playlist[0]
        emojis      = playlist[1]
        scraper     = YoutubePlaylists(self.admin, emojis)
        scraper.get(playlist_id)
        self.admin.orm.api.state.playlist_index = index + 1
        return len(playlists)


    def _get_stream(self):

        ystream  = self.admin.orm.api.youtube.read(type="stream", Xid=True)
        database = self.admin.orm.api.youtube.read(type="stream", posted=True)
        index    = self.admin.orm.api.state.ystream_index
        
        try:
            assert len(ystream)
            ystream = ystream[index]
        except IndexError:
            self.admin.orm.api.state.ystream_index = index = 0
            ystream = ystream[index]
        except AssertionError:
            t = datetime.now() + timedelta(hours = 2)
            self.admin.orm.api.state.ystream_delta = t
            message = "No YouTube RSS streams are registered."
            self.admin.orm.api.messages.create(message, "youtube")
            log.debug(f"{self.admin.name}\n{message}")
            raise AssertionError

        channel_id = ystream[0]
        emojis     = ystream[1]
        flags      = ystream[2]
        scraper    = RSSStreamer(self.admin, emojis, flags)
        try:
            stream = scraper.get(channel_id)
        except requests.exceptions.ConnectionError:
            n = random.randint(30, 90)
            delta = datetime.utcnow() + timedelta(minutes = n)
            self.admin.orm.api.state.ystream_delta = delta
            raise RateLimitException
        stream = self._append_is_tweeted_ystream_values(stream, database)
        self._update_ystream_content(stream, channel_id, database)
        self.admin.orm.api.state.ystream_index = index = index + 1
        return len(ystream)


    def _append_is_tweeted_ystream_values(self, stream, database):
        for e, video in enumerate(stream):
            for record in database:
                if (video[4] == record[4]):
                    video = video[:9] + (True,)
                    stream[e] = video
                    break
        return stream


    def _update_ystream_content(self, stream, channel_id, database):
        for video in database:
            if (video[2] == channel_id):
                self.admin.orm.api.youtube.delete(video[4])
        self.admin.orm.api.youtube.create(stream)
