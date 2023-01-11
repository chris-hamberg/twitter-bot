from model.M.engage.compositors.filter_compositor import FilterCompositor

from model.M.engage.type_epsilon.interface import ScraperTypeEpsilon
from model.M.engage.reply.rtype1.core import ReplyType1Core

from model.objects.exceptions import MonthlyRateLimitException
from model.objects.exceptions import RateLimitException
from model.objects.normalize import normalize

from model.M.super.superclass import SuperManager

from datetime import datetime
import logging


log = logging.getLogger(__name__)


class ReplyType1Manager(SuperManager):


    def __init__(self, admin):
        super().__init__()
        self._params = {"type": "reply_type1", "liked": False, "replied": False,
                "mentioned": False}
        self._scraper  = ScraperTypeEpsilon(admin)
        self._filter   = FilterCompositor(admin)
        self._core     = ReplyType1Core(admin)
        self.admin     = admin
        self.name      = "reply_type1"


    def execute(self):
        tweets = None; self._update_config()
        if self._sentinel_type1(): return False
        if self._sentinel_type2(): self._scraper.scrape(); return False
        if not self._sentinel_type3():
            tweets = self.admin.orm.api.tweets.read(**self._params)
            tweets.sort(key = lambda t: normalize(t[-1])); tweets.reverse()
        if (not tweets): self._scraper.scrape()
        else:            self._core.engage(tweets)


    def _update_config(self):
        self._filter.refresh_blacklisted_users()
        self._filter.refresh_keywords()
        self._filter.refresh_blacklist()


    def _sentinel_type1(self):
        if self._filter._keywords: return False
        message = "Can't decide which tweets to engage without keywords."
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")
        self._set_timestamp(minutes = 30)
        return True


    def _sentinel_type2(self):
        delta = normalize(self.admin.orm.api.state.reply_type1_delta)
        now   = datetime.utcnow()
        if (now <= delta) and (now.hour >= 6) and (now.hour <= 16):
            if 240 <= (delta - datetime.utcnow()).total_seconds():
                return True
        return False


    def _sentinel_type3(self):
        C1 = 21 <= self.admin.orm.api.state.retweet_reply_count
        C2 = 28 <= self.admin.orm.api.state.like_subcycle_count
        C3 = 15 <= self.admin.orm.api.state.reply_count       
        if not any([C1, C2, C3]): return False
        self._set_timestamp(minutes = 60)
        return True
