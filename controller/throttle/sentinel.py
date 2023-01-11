from model.M.engage.tweets.preprocessor import TweetPreprocessor
from model.objects.exceptions import SentinelException
from model.objects.normalize import normalize
from datetime import timedelta
from datetime import datetime
import random


class EngagementSentinel:


    def enforce(self, manager, admin):
        delta = None
        self._state(manager, admin)
        self._ensure_tweets()
        message = "The bot is pretending to be a human, and asleep."
        if not self._sentinel():
            n       = random.randint(7, 20)
            delta   = datetime.utcnow() + timedelta(minutes = n)
            self._reset_state(delta)
            self._tweet(message, delta)
            self._set(delta, message)
        return self._close(delta, message)


    def _close(self, delta, message):
        if not (self.manager.name == "reply_type1"): return False
        elif delta: 
            self.admin.orm.api.messages.create(message, "retweets")
            return True
        else: 
            self.admin.orm.api.messages.create("Awaiting engagement.", "retweets")
            return False


    def _set(self, delta, message):
        if (self.manager.name != "tweet"):
            setattr(self.admin.orm.api.state, f"{self.manager.name}_delta", delta)
            self.admin.orm.api.messages.create(message, self.manager.name)
        if (self.manager.name != "reply_type1"): raise SentinelException


    def _tweet(self, message, delta):
        if not (self.manager.name == "tweet"): return False
        params = {"liked": False, "replied": False, "mentioned": False}
        C1 = self.admin.orm.api.tweets.count(type = "tweetAI", **params) < 50
        C2 = normalize(self.admin.orm.api.state.tweet_delta) < datetime.utcnow()
        if (C1) and (C2):
            t = getattr(self.admin.orm.api.state, f"{self.manager.name}_delta")
            if (normalize(t) < datetime.utcnow()):
                tweetAI = TweetPreprocessor(self.admin)
                tweetAI._get_ai_tweet()
                n = random.randint(20, 60)
                delta = datetime.utcnow() + timedelta(minutes = n)
                self.admin.orm.api.state.tweet_delta = delta
            else:
                self.admin.orm.api.messages.create("rate limit", self.manager.name)
        elif (C1) and (not C2):
            message = "rate limit"
            self.admin.orm.api.messages.create(message, self.manager.name)
        else:
            self.admin.orm.api.state.tweet_delta = delta
            self.admin.orm.api.messages.create(message, self.manager.name)


    def _sentinel(self):
        if (datetime.utcnow().hour >= 6) and (datetime.utcnow().hour <= 16):
            return False
        else: return True


    def _state(self, manager, admin):
        self.manager = manager
        self.admin   = admin


    def _ensure_tweets(self):
        if not (self.manager.name == "tweet"): return False
        params = {"liked": False, "replied": False, "mentioned": False}
        if self.admin.orm.api.tweets.count(type = "tweetAI", **params): 
            return False
        tweetAI = TweetPreprocessor(self.admin)
        tweetAI._get_ai_tweet()


    def _reset_state(self, delta):
        counts = [self.admin.orm.api.state.retweet_reply_count,
                  self.admin.orm.api.state.like_subcycle_count,
                  self.admin.orm.api.state.reply_count]
        if any(counts):
            self.admin.orm.api.state.tweet_delta = delta
            self.admin.orm.api.state.retweet_reply_count = 0
            self.admin.orm.api.state.like_subcycle_count = 0
            self.admin.orm.api.state.reply_count         = 0
