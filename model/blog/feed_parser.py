from io import BytesIO
import feedparser
import requests
import logging


log = logging.getLogger(__name__)


class Blog:


    def __init__(self, admin):
        self.admin = admin
        self.name  = "blog"
    

    def parse(self):
        index    = self.admin.orm.api.state.blog_index
        length   = self.admin.orm.api.blog.count(feeds = True)
        if   (not length)     : return False
        elif (length <= index): self.admin.orm.api.state.blog_index = index = 0
        urls     = self.admin.orm.api.blog.read(feeds = True)
        url      = urls[index][0]
        response = self.request(url)
        if not response: return index
        content  = BytesIO(response.content)
        feed     = feedparser.parse(content)
        #code     = feed.get("status")
        code     = r.status_code
        domain   = url.split("://")[-1]
        message  = f"HTTP {code}: {domain}"
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")
        if code and (int(code) == 200): self._update(feed, url)
        return index


    def request(self, url):
        try: 
            r = requests.get(url, timeout = 10.0)
            return r
        except requests.ReadTimeout:
            m = f"Timeout: {url}"
            self.admin.orm.api.messages.create(m, self.name)
            return None


    def _update(self, feed, url):
        feed      = self._construct(feed, url)
        database  = self.admin.orm.api.blog.read(posted = True)
        for article in feed.get("entries"):
            for record in database:
                if (article[0] == record[3]):
                    article.append(True)
                    break
            else:
                article.append(False)
        feed_url = feed.get("feed_url")
        self.admin.orm.api.blog.delete(feed_url)
        self.admin.orm.api.blog.create(feed)


    def _construct(self, feed, url):
        entries    = []
        feed_title = feed.feed.get("title")
        feed_url   = url
        for article in feed.get("entries"):
            article_title   = article.get("title")
            article_author  = article.get("author")
            article_summary = article.get("summary")
            article_url     = article.get("link")
            entries.append([article_url, article_title, article_author, 
                    article_summary])
        feed = {"feed_title": feed_title, "feed_url": feed_url, 
                "entries": entries}
        return feed
