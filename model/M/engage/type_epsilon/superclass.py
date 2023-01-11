from model.M.engage.type_epsilon.preprocessor import TypeEpsilonPreprocessor
from model.M.engage.compositors.filter_compositor import FilterCompositor

from model.M.parser.conversation_processor import ConversationProcessor
from model.M.parser.interface import TweetParser

from model.M.super.superclass import SuperManager

from model.objects.exceptions import RateLimitException
from model.objects.normalize import normalize

from model.twitter.get_tweets import GetTweets

from datetime import timedelta
from datetime import datetime
import random
import time


class SuperTypeEpsilon(SuperManager):


    def __init__(self, admin):
        super().__init__()
        self._preprocessor = TypeEpsilonPreprocessor(admin)
        self._c_processor  = ConversationProcessor(admin)
        self._get_tweets   = GetTweets().request
        self._parser       = TweetParser(admin)
        self._filter       = FilterCompositor(admin)
        self.admin         = admin
        self.name          = "type_epsilon"


    def scrape(self): raise NotImplemented


    def _core(self, followers, e, supercycle, subcycle):
        id, tweets = self._request(followers, supercycle)
        if self._validate(tweets): 
            e = self._subReport(e, id, tweets, followers, supercycle)
        subcycle, supercycle = self._cycle_state(subcycle, supercycle)
        return e, supercycle, subcycle


    def _close(self, e):
        if e: self.report(f"Scraped {e} tweets from followers.")
        else: self.report("No tweets found from followers (this is ok.)")
        delta = datetime.utcnow() + timedelta(minutes = random.randint(15, 45))
        self.admin.orm.api.state.type_epsilon_subcycle_delta = delta


    def _cycle_state(self, subcycle, supercycle):
        state = self.admin.orm.api.state
        state.type_epsilon_subcycle_index   = subcycle   = subcycle   + 1
        state.type_epsilon_supercycle_index = supercycle = supercycle + 1
        time.sleep(0.1)
        return subcycle, supercycle


    def _delta_sentinel(self):
        delta = self.admin.orm.api.state.type_epsilon_subcycle_delta
        if datetime.utcnow() <= normalize(delta): 
            self.admin.orm.api.messages.create("rate limit", self.name)
            return True
        else: return False


    def _subReport(self, e, id, tweets, followers, supercycle):
        count = self._process(id, tweets)
        if not count: return e
        e += count
        self.report(f"Scraped {count} tweets from {followers[supercycle][1]}.")
        time.sleep(3)
        self.report("Searching for tweets from followers.")
        return e


    def _process(self, id, tweets):
        convos    = self._parser.parse(tweets, type = "reply_type1")
        tweets, _ = self._c_processor.proc(convos, self._filter.filter)
        tweets    = self._drop_redundant(tweets)
        self.admin.orm.api.tweets.create(tweets)
        return len(tweets)
        

    def _validate(self, tweets):
        if (tweets.status_code == 429):
            n = random.randrange(15, 60)
            self._set_timestamp(minutes = n)
            self._set_timestamp(minutes = n, name = "inactive")
            self.report("Request tweets are rate limted.")
            raise RateLimitException
        elif (400 <= tweets.status_code <= 403):
            self.report(f"Request tweets: HTTP {tweets.status_code}")
            return False
        elif (200 <= tweets.status_code < 300): return True


    def _request(self, followers, supercycle):
        id     = followers[supercycle][0]
        epoch  = datetime.utcnow() - timedelta(days = 7)
        epoch  = datetime.strftime(epoch, "%Y-%m-%dT%H:%M:%SZ")
        tweets = self._get_tweets(id, self.admin.auth, 5, epoch, history = True)
        return id, tweets


    def _drop_redundant(self, tweets):
        xQ = []
        for tweet in tweets:
            if self.admin.orm.api.tweets.read(tweet[0]): continue
            else: xQ.append(tweet)
        return xQ
