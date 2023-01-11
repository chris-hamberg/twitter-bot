from model.M.engage.tweets.objects.super import SuperTweetObject
from datetime import timedelta
from datetime import datetime
import random


class tweetAI(SuperTweetObject):


    def __init__(self, admin): super().__init__(admin)


    def execute(self):
        if not self.admin.orm.api.state.tweetAI_subcycle_index:
            self._set_subcycle_injection()
        if self.admin.orm.api.state.tweetAI_injection_state:
            if self._decide_injection(): return "inject", "Λ"
        tweet = self.preprocessor.get("tweetAI")
        _ = self._subexecution_type1(tweet[1])
        r = self._post(); tweet = self._postproc(r, tweet)
        self._report(r, "tweetAI"); self._terminate(r)
        return r, tweet


    def _terminate(self, r):
        super()._terminate(r)
        if not self.admin.orm.api.state.tweetAI_subcycle_index:
            self.admin.orm.api.state.tweetAI_injection_state = False


    def _postproc(self, r, tweet):
        if (200 <= r.status_code < 300):
            tweet_id        = r.json().get("data").get("id")
            conversation_id = tweet_id
            self.admin.orm.api.tweets.delete(tweet[0])
            tweet = (tweet_id,) + tweet[1:4] + tweet[7:9] + (conversation_id,)
            self.admin.orm.api.tweets.create([tweet])
            self.admin.orm.api.tweets.update(tweet_id)
        return tweet


    def _set_subcycle_injection(self):
        p = round(random.random() * 100, 2)
        if   (p <= 50): n = 1
        elif (p <= 85): n = 2
        else:           n = 3
        self.admin.orm.api.state.tweetAI_injection_state = True
        self.admin.orm.api.state.tweetAI_subcycle_index  = n


    def _decide_injection(self):
        base = self.admin.orm.api.state.tweetAI_subcycle_index
        if (base == 3): threshold = 33
        if (base == 2): threshold = 22
        if (base == 1): threshold = 11
        else:           threshold =  0
        if round(random.random() * 100, 2) <= threshold: return True
        return False
