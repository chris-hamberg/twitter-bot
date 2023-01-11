from model.M.engage.compositors.filter_compositor import FilterCompositor
from model.M.engage.compositors.like_compositor import LikeCompositor
from model.M.engage.tweets.preprocessor import TweetPreprocessor
from model.M.engage.retweets import RetweetManager

from model.objects.exceptions import ConfigurateXType4Ex
from model.objects.exceptions import RateLimitException
from model.objects.exceptions import NullValue
from model.objects.normalize import normalize

from model.twitter.tweet import Tweet
from datetime import timedelta
from datetime import datetime
from math import ceil
import logging
import random
import time
import os


log = logging.getLogger(__name__)


class ReplyType2Manager:


    def __init__(self, admin):
        self.admin    = admin
        self.name     = "reply_type2"
        self._tweet   = Tweet().request
        self._like    = LikeCompositor(admin)
        self._retweet = RetweetManager(admin).retweet
        self._format  = TweetPreprocessor(admin)._format_tweet
        self._filter  = FilterCompositor(admin)


    def execute(self, depth = 4):
        self.validate()
        tweets = self.admin.orm.api.tweets.read(replied = False, type = "reply_type2")
        reply_count, recursion = self.admin.orm.api.state.reply_count, False
        if ((not tweets) or (10 - reply_count <= 0)):
            self._close(tweets, supercycle = True); return False
        tweets.sort(key = lambda t: normalize(t[-1])); tweets.reverse()
        tweet, text = tweets[0], self._get_content()
        username, p = self._get_username(tweet), random.random() * 100
        if (depth != 4): p *= 4
        if ((self.admin.orm.api.state.reply_probability_type2 < p) or (
                self._filter.filter(tweet[1], user = username))):
            self._state(tweet = tweet)
            recursion = self._close(tweets, skip = True, depth = depth)
            if recursion: self.execute(depth - 1)
            return False
        #reply_chance = self._decide_response_type(tweet)
        r = self._reply(text, tweet[0], username, 1)
        self._state(r, tweet, 1) 
        recursion = self._close(tweets, depth = depth)
        if recursion: self.execute(depth - 1)


    def _close(self, tweets, skip = False, depth = 1, supercycle = False):
        self._probability(tweets)
        if (not supercycle):
            n = self._delta(tweets, depth)
            if ((not n) and (depth)): return True
            else: delta = datetime.utcnow() + timedelta(seconds = n)
        else: delta = datetime.utcnow() + timedelta(hours = 1)
        self.admin.orm.api.state.reply_type2_delta = delta
        if (skip):
            reply_p = self.admin.orm.api.state.reply_probability_type2
            size = len(tweets)
            m = f"{size} tweets \u2208 \u03C7Q;   (\u03C3-reply) {reply_p}%"
            if (not depth):
                m += "    TURBO"
            self.admin.orm.api.messages.create(m, self.name)
            log.debug(f"{self.admin.name}\n{m}")
        return False


    def _probability(self, tweets):
        cardinality  = len(tweets)
        reply_target = 10 - self.admin.orm.api.state.reply_count
        if (reply_target < 0): reply_target = 0
        reply_p = round(reply_target/cardinality*100, 2) if cardinality else 0
        self.admin.orm.api.state.reply_probability_type2 = reply_p


    def _delta(self, tweets, depth):
        period = list(range(16, 24)) + list(range(6))
        hours  = (len(period) - 1) - period.index(datetime.utcnow().hour)
        if (not hours): hours = 1
        cardinality = len(tweets)
        rate = cardinality / hours if cardinality else 1
        rate = (60 * 60) / ceil(rate)
        rate -= 22 if (0 <= rate - 22) else 0
        if ((rate - 22 < 0) and (depth)): return False
        distance = abs(22 - rate)
        m, n = max(0, (rate - distance)), max(1, (rate + distance))
        m, n = int(m), int(n)
        return 0 if not m else random.randint(m, n)


    def _decide_response_type(self, tweet):
        reply_count  = self.admin.orm.api.state.reply_count
        epoch        = datetime.utcnow() - timedelta(days = 1)
        delta        = normalize(tweet[-1])
        p            = 1 if (delta <= epoch) else random.random()
        return (p <= 0.20) if (reply_count <= 10) else False


    def _reply(self, text, tweet_id, username = None, reply_chance = None):
        params = {"tweet": text, "token": self.admin.bearer} 
        params.update({"auth": self.admin.auth})
        if reply_chance: params.update({"tweet_id": str(tweet_id)})
        elif username:   params.update({"tweet": f"@{username} {text}"})
        else: return False
        return self._tweet(**params)


    def _get_content(self):
        path = os.path.join("tweets",f"{self.admin.username}","reply_text.txt")
        with open(path, "r") as fhand: return self._format(fhand.read())


    def _state(self, r = False, tweet = None, reply_chance = False):
        self.admin.orm.api.tweets.update(tweet[0])
        if r and (200 <= r.status_code < 300):
            #if reply_chance: 
            reply_count = self.admin.orm.api.state.reply_count
            self.admin.orm.api.state.reply_count = reply_count + 1

            self._record(r, tweet)
            message = f"Replied to {tweet[0]}"
            self.admin.orm.api.messages.create(message, self.name)
            log.debug(f"{self.admin.name}\n{message}")
            time.sleep(random.randint(1, 3))
            self._like.tweets_by_ids([tweet[0]], self.name)
            time.sleep(random.randint(1, 3))
            self._retweet(tweet, name = self.name)
            time.sleep(random.randint(1, 3))


    def _get_username(self, tweet):
        uid, tid = tweet[2], tweet[0]
        try: return self.admin.orm.api.tweets.user(id=uid, tweet_id=tid)[0][2]
        except IndexError: return None


    def _record(self, r, tweet):
        tweet_id        = r.json().get("data").get("id")
        text            = r.json().get("data").get("text")
        id              = self.admin.id
        admin           = self.admin.id
        type            = "response"
        query           = None
        conversation_id = tweet[0]
        tweet = [(tweet_id, text, id, admin, type, query, conversation_id)]
        self.admin.orm.api.tweets.create(tweet)
        self.admin.orm.api.tweets.update(tweet_id)


    def validate(self):
        path = os.path.join("tweets",f"{self.admin.username}","reply_text.txt")
        with open(path, "r") as fhand: text = fhand.read()
        if bool(text): return True
        else: message = "Static reply requires content in reply_text.txt"
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")
        self._close([], supercycle = True)
        raise ConfigurateXType4Ex
