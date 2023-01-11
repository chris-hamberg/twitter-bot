from model.M.engage.compositors.filter_compositor import FilterCompositor
from model.M.parser.conversation_processor import ConversationProcessor
from model.M.parser.interface import TweetParser

from model.twitter.search_tweets import SearchTweets

from model.objects.exceptions import RateLimitException
from model.objects.normalize import normalize

from datetime import timedelta
from datetime import datetime
import logging
import random


log = logging.getLogger(__name__)


class ScraperTypeGamma:


    def __init__(self, admin):
        self.admin    = admin
        self._c_processor = ConversationProcessor(admin)
        self._request     = SearchTweets().request
        self._parser      = TweetParser(admin)
        self._filter      = FilterCompositor(admin).filter
        self.name         = "type_gamma"
        self.q            = f"@{admin.username}"
        self.params       = {"auth": admin.auth, "history": True, 
                "query": self.q}


    def execute(self):
        self._sentinel_type_1(); self.c = 0 
        self._polling(); r = self._subscrape()
        if (200 <= r.status_code < 300): self._persist(r)
        self._delta(); self._report(r)


    def _sentinel_type_1(self):
        # NOTE this is hypothetically redundant
        delta = normalize(self.admin.orm.api.state.type_gamma_delta)
        if datetime.utcnow() <= delta: raise RateLimitException


    def _sentinel_type_2(self, mention, username):
        if self.admin.orm.api.tweets.read(mention[0]): return True
        username = self.admin.orm.api.tweets.user(mention[3], mention[0])
        if self._filter(mention[1], user = username, mentions = True):
            self.admin.orm.api.tweets.create([mention])
            self.admin.orm.api.tweets.type_gamma_update(mention[0])
            self.c += 1; return True


    def _delta(self):
        delta = datetime.utcnow() + timedelta(hours  = random.randint(2, 3))
        self.admin.orm.api.state.type_gamma_delta = delta


    def _report(self, r):
        if self.c:
            m = f"Scraper type-Γ found {self.c} mentions @{self.admin.username}"
        else: m = f"Scraper type-Γ HTTP {r.status_code}"
        self.admin.orm.api.messages.create(m, self.name)
        log.debug(f"{self.admin.name}\n{m}")


    def _polling(self):
        since_id = self.admin.orm.api.tweets.polling(type = "mention")
        self.params.update({"since_id": since_id})


    def _HTTPxxx(self, r):
        if (200 <= r.status_code < 300):      return True
        elif not self.params.get("since_id"): return True
        elif ((r.status_code == 400) and (r.json().get("errors"))):
            errors  = r.json().get("errors")[0]
            message = errors.get("message")
            if "since_id" in message: self.params.update({"since_id": None})
        return bool(self.params.get("since_id"))


    def _subscrape(self):
        while True:
            r = self._request(**self.params)
            if self._HTTPxxx(r): return r
            else: continue


    def _persist(self, r):
        convos      = self._parser.parse(r, type = "mention", query = self.q)
        mentions, _ = self._c_processor.proc(convos, self._sentinel_type_2)
        self.c     += len(mentions)
        self.admin.orm.api.tweets.create(mentions)
