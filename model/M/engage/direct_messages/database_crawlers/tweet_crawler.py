from model.managers.database_crawlers.super_crawler import SuperCrawler
from model.objects.exceptions import UnhandledHTTPException
from model.objects.exceptions import RateLimitException
from model.twitter.get_tweets import GetTweets
import logging
import random
import time
import re


log = logging.getLogger(__name__)

#NOTE For DMs. DM is not supported by API v2. So this is not used.
class TweetCrawler(SuperCrawler):


    def __init__(self, admin):
        super().__init__(admin)
        self._get_tweets = GetTweets().request
        self.name  = "tweet crawler"
        self._patterns = [
                r"my.*mix.*tape", r"my.*album", r"in.*the.*studio",
                r"record.*my.*mix.*tape", r"record.*my.*album"
                ]


    def execute(self):
        interface, c, p = self.admin.orm.api, "followers", "dm_queue"
        followers = interface.users.read(category = c, dm_queue = False)
        if not len(followers): self._break(days = 6)
        index  = interface.state.tweet_crawler_index
        while (index < len(followers)):
            id = followers[index][2]
            r  = self._handler(id)
            if self._parse(r):
                message = f"{id} has a tweet with KEYWORDS. Updating database."
                interface.users.update(p = p, val = True, id = id, category = c)
                index += 1
            else:
                message = f"{id} does not have tweets with KEYWORDS."
                interface.state.tweet_crawler_index = index = index + 1
            interface.messages.create(message, self.name)
            log.debug(f"{self.admin.name}\n{message}")
            self._throttle(index)
        else:
            interface.state.tweet_crawler_index = 0
            self._break(minutes = 60)


    def _parse(self, r):
        if (not r): 
            return False
        elif (not r.json().get("data")): 
            return False
        for tweet in r.json().get("data"):
            text = tweet.get("text")
            if ("RT" in text): continue
            text = text.lower()
            for regex in self._patterns:
                patterns = re.findall(regex, text)
                if (not patterns): continue
                else: return True
        return False


    def _throttle(self, index):
        if (not index % 50):
            self._break(minutes = 60)
        t = random.randint(1, 3)
        time.sleep(t)


    def _handler(self, id):
        r = self._get_tweets(id, self.admin.auth, max_results = 100)
        return super()._handler(r)
