from model.M.engage.compositors.filter_compositor import FilterCompositor
from model.M.super.superclass import SuperManager

from model.M.parser.conversation_processor import ConversationProcessor
from model.M.parser.interface import TweetParser

from model.objects.exceptions import ForbiddenException

from datetime import timedelta
from datetime import datetime
import random


class ScraperTypeLambda(SuperManager):


    def __init__(self, admin):
        super().__init__()
        self.params       = {"page": None, "auth": admin.auth, "query": None}
        self.params.update( {"history": True})
        self.name         = "type_lambda"
        self.admin        = admin
        self._c_processor = ConversationProcessor(admin)
        self._filter      = FilterCompositor(admin)
        self._parser      = TweetParser(admin)


    def execute(self):
        self._validate(); self._blacklist = self._filter._blacklist
        index = self.admin.orm.api.state.type_lambda_index
        query = self.admin.orm.api.queries[index]
        beta  = self.admin.orm.api.tweets.count()
        gamma = self.admin.orm.api.type_alpha.count()
        self.params.update({"query": f'"{query.q}"', "page": query.pagination})
        if query.polling: self.params.update({"since_id": str(query.polling)})
        self.report(f"Searching for '{query.q}'.")
        try:
            r = self._handler(**self.params)
            if not r.json().get("meta").get("result_count"):
                self.report(f"No results for '{query.q}'")
        except ForbiddenException:
            self.report("HTTP 403 Forbidden")
            self._set_timestamp()
            raise ForbiddenException
        conversations  = self._parser.parse(r, query = query)
        tweets, hcount = self._c_processor.proc(conversations, self._sentinel)
        self.admin.orm.api.type_alpha.create(r, priority = 1)
        self.admin.orm.api.tweets.create(tweets)
        alpha   = self.admin.orm.api.tweets.count()
        epsilon = self.admin.orm.api.type_alpha.count()
        t_count, u_count = (alpha - beta) - hcount, (epsilon - gamma)
        self.report(f"Found {t_count} tweets & {u_count} users for '{query.q}'")
        query.pagination = r; self._state(query, index)


    def _state(self, query, index):
        orm = self.admin.orm
        if not query.pagination: query.polling = orm.api.tweets.polling(query.q)
        orm.api.state.type_alpha_count = orm.api.type_alpha.count()
        orm.api.state.type_lambda_index = (index + 1) % len(orm.api.queries)
        delta = datetime.utcnow() + timedelta(minutes = random.randint(20, 40))
        orm.api.state.type_lambda_delta = delta


    def _validate(self):
        try: assert self.admin.orm.api.queries
        except AssertionError:
            self.report("No search queries registered. Sleeping 2 hours.")
            delta = datetime.utcnow() + timedelta(minutes = 120)
            self.admin.orm.api.state.type_lambda_delta = delta
            raise RateLimitException


    def _sentinel(self, tweet, username):
        for blacklisted in self._blacklist:
            blacklisted = blacklisted.lower()
            text        = tweet[1].lower()
            if text.count(blacklisted): return True
