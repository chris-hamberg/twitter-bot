from model.objects.exceptions import UnhandledHTTPException
from model.objects.exceptions import RateLimitException
from datetime import timedelta
from datetime import datetime
import traceback
import logging


log = logging.getLogger(__name__)

#NOTE For DMs. DM is not supported by API v2 so this is not used.
class SuperCrawler:


    def __init__(self, admin):
        self.admin = admin


    def execute(self):
        raise NotImplementedError


    def _parse(self, r):
        raise NotImplementedError


    def _break(self, min = 15, days = None, exception = RateLimitException):
        if days:
            ts = datetime.utcnow() + timedelta(days = days)
        else:
            ts = datetime.utcnow() + timedelta(minutes = minutes)
        self.admin.orm.api.state.tweet_crawler_delta = ts
        raise exception


    def _handler(self, r):
        try:
            if (r.status_code == 200):
                return r
            elif (r.status_code == 429):
                self._break(min = 60)
            elif ((r.status_code == 400) or (r.status_code == 403)):
                return False
            else:
                log.debug("{self.admin.name}\nHTTP {r.status_code}")
                self._break(min = 60, exception = UnhandledHTTPException)
        except AttributeError:
            e = traceback.format_exc()
            log.error(f"{self.admin.name}\n{e}")
            sys.exit(0)
