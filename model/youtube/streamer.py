try:
    from model.youtube.youtube import Youtube
except ModuleNotFoundError:
    from youtube import Youtube
import xml.etree.ElementTree as etree
import requests
import logging


log = logging.getLogger(__name__)


class RSSStreamer(Youtube):


    def __init__(self, admin, emojis = None, flags = None, p = None):
        super().__init__(admin, emojis, p)
        self.base_url = "https://www.youtube.com/feeds/videos.xml?channel_id={id}"
        self.video_url = "https://www.youtube.com/watch?v={video}"
        self.slug1 = "{http://www.w3.org/2005/Atom}"
        self.slug2 = "{http://www.youtube.com/xml/schemas/2015}"
        self.type  = "rss"
        self.flags = flags


    def get(self, channel_id):
        url = self.base_url.format(id = channel_id)
        r = requests.get(url)
        stream = self.parse(r.content, channel_id)
        message = (f"HTTP {r.status_code}: {len(stream)} videos for channel "
                  f"{channel_id}")
        self.admin.orm.api.messages.create(message, "youtube")
        log.debug(f"{self.admin.name}\n{message}")
        return stream


    def parse(self, content, channel_id):
        stream, playlist_id = [], None
        tree = etree.fromstring(content)
        for element in tree:
            if "entry" in element.tag:
                video_id = element.find(self.slug2 + "videoId").text
                title    = element.find(self.slug1 + "title").text
                if self.filter(title):
                    continue
                else:
                    url = self.video_url.format(video = video_id)
                    video = (self.type, self.admin.id, channel_id, playlist_id,
                             video_id, title, url, self.emojis, 
                             self.flags or None, False)
                    stream.append(video)
        return stream


    def filter(self, title):
        try:
            flags = self.flags.split(",")
        except AttributeError:
            return False
        else:
            for flag in self.flags.split(","):
                if (flag == ""): continue
                if flag in title:
                    return True
                else:
                    return False
