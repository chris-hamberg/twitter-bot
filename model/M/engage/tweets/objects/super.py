from model.M.engage.tweets.preprocessor import TweetPreprocessor
from model.objects.exceptions import UnexpectedLogicalError
from model.objects.exceptions import StatusCodeException
from model.objects.exceptions import NullValue
from model.twitter.tweet import Tweet
from datetime import timedelta
from datetime import datetime
import logging
import random


log = logging.getLogger(__name__)


class SuperTweetObject:


    def __init__(self, admin):
        self.preprocessor = TweetPreprocessor(admin)
        self.tweet        = Tweet().request
        self.admin        = admin
        self.name         = "tweet"
        self.params       = {"token": admin.bearer, "auth": admin.auth}


    def execute(self): raise NotImplemented


    def _subexecution_type1(self, tweet):
        self._validate(tweet); self.params.update({"tweet": tweet})


    def _subexecution_type2(self, type, media = None):
        r = self._post(); self._record(r, type); self._report(r, type, media)
        if not (200 <= r.status_code < 300): raise StatusCodeException
        return r


    def _get_delta(self):
        if self.admin.orm.api.state.tweetAI_subcycle_index:
            return timedelta(  seconds = random.randint(30, 300))
        else: return timedelta(minutes = random.randint(1, 25))


    def _update_subcycle_index(self):
        if self.admin.orm.api.state.tweetAI_subcycle_index:
            index = self.admin.orm.api.state.tweetAI_subcycle_index
            self.admin.orm.api.state.tweetAI_subcycle_index = index - 1


    def _post(self):
        try: return self.tweet(**self.params)
        except ForbiddenException:
            message = "HTTP 403 Forbidden."
            self.admin.orm.api.messages.create(message, self.name)
            log.debug(f"{self.admin.name}\n{message}")
            delta = datetime.utcnow() + timedelta(minutes = 15)
            self.admin.orm.api.state.tweet_delta = delta
            raise ForbiddenException


    def _terminate(self, r):
        if (r and r.json().get("errors")): delta = timedelta(minutes = 0)
        else: delta = self._subdelegate()
        delta = datetime.utcnow() + delta
        self.admin.orm.api.state.tweet_delta = delta


    def _subdelegate(self):
        count = self.admin.orm.api.state.tweet_count
        self.admin.orm.api.state.tweet_count = count + 1
        self._update_subcycle_index()
        return self._get_delta()


    def _validate(self, tweet):
        if not bool(tweet):
            delta   = datetime.utcnow() + timedelta(hours = 1)
            message = "No {self.__class__.__name__} tweets exist for tweeting."
            self.admin.orm.api.messages.create(message, self.name)
            log.debug(f"{self.admin.name}\n{message}")
            raise NullValue


    def _record(self, r, type):
        if (200 <= r.status_code < 300):
            tweet_id        = r.json().get("data").get("id")
            text            = r.json().get("data").get("text")
            id              = self.admin.id
            admin           = self.admin.id
            type            = type
            query           = None
            conversation_id = tweet_id
            tweet = [(tweet_id, text, id, admin, type, query, conversation_id)]
            self.admin.orm.api.tweets.create(tweet)
            self.admin.orm.api.tweets.update(tweet_id)


    def _report(self, r, type, media = None):
        if not r: raise UnexpectedLogicalError
        elif (200 <= r.status_code < 300): message = f"Tweeted {type} content."
        elif (r.status_code == 400):
            info    = media or type
            message = r.json().get("errors")[0].get("message")
            message = f"{message[:-1]}: {info}"
        else: message = f"HTTP {r.status_code}: {type}"
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")
