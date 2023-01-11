from model.managers.database_crawlers.super_crawler import SuperCrawler
from model.objects.exceptions import UnhandledHTTPException
from model.objects.exceptions import RateLimitException
from model.twitter.lookup_id import LookupID
import logging
import random
import time


log = logging.getLogger(__name__)

#NOTE For DMs. DM is not supported by API v2 so this is not used.
class ProfileCrawler(SuperCrawler):


    def __init__(self, admin):
        super().__init__(admin)
        self._request = LookupID().request
        self.name     = "profile crawler"


    def execute(self):
        c = "followers"
        users = self.admin.orm.api.users
        followers = users.read(category = "followers", parsed = False)
        if not len(followers): self._break(days = 6)
        for follower in followers[:100]:
            id = follower[2]
            r, t = self._handler(id), random.randint(1, 3)
            if self._parse(r):
                message = f"{id} profile contains KEYWORDS. Updating database."
                for p in ("dm_queue", "parsed"):
                    users.update(p = p, val = True, id = id, category = c)
            else:
                message = (f"{follower} profile has no KEYWORDS. "
                           f"Sleeping {t} seconds.")
                users.update(p = "parsed", val = True, id = id, category = c)
            self.admin.orm.api.messages.create(message, self.name)
            log.debug(f"{self.admin.name}\n{message}")
            time.sleep(t)
        else:
            self._break(minutes = 60)


    def _parse(self, r):
        #TODO
        d = r.json().get("data").get("description")
        if (((" rap" in d.lower()) or (("music" in d.lower()))) and (
            " rape" not in d.lower()) and (" rapist" not in d.lower())):
            return True


    def _handler(self, id):
        r = self._request(id, self.admin.auth)
        return super()._hander(r)
