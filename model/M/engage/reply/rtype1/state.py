from model.M.super.superclass import SuperManager
from datetime import datetime
from math import ceil
import traceback
import random
import time


class ReplyType1StateManager(SuperManager):


    def __init__(self, admin):
        super().__init__()
        self.admin = admin
        self.name  = "reply_type1"


    def manage(self, tweets, skip = False, recursion = 0):
        self._p(tweets)
        n = self._delta(tweets, recursion)
        if (recursion < 4) and (not n): return False
        self._set_timestamp(seconds = n)
        if skip:
            like_p    = self.admin.orm.api.state.like_probability
            reply_p   = self.admin.orm.api.state.reply_probability
            size      = len(tweets)
            m = (f"{size} tweets \u2208 \u03C7Q;   (\u03C3-like) {like_p}% "
                 f"  (\u03C3-reply/retweet) {reply_p}%")
            if recursion: m = f"{m}   TURBO"
            self.report(m)
        return True


    def _p(self, tweets):
        cardinality          = len(tweets)
        retweet_reply_target = 21 - self.admin.orm.api.state.retweet_reply_count
        like_target          = 28 - self.admin.orm.api.state.like_subcycle_count

        if (retweet_reply_target < 0): retweet_reply_target = 0
        if (like_target          < 0): like_target          = 0
        if cardinality:
            retweet_reply_p = round((retweet_reply_target / cardinality) *100,2)
            like_p          = round((like_target          / cardinality) *100,2)
        else: retweet_reply_p = like_p = 0

        self.admin.orm.api.state.like_probability    = like_p
        self.admin.orm.api.state.reply_probability   = retweet_reply_p
        self.admin.orm.api.state.retweet_probability = retweet_reply_p


    def _delta(self, tweets, recursion):
        period = list(range(16, 24)) + list(range(6))
        hours  = (len(period) - 1) - period.index(datetime.utcnow().hour)
        if not hours: hours = 1
        cardinality = len(tweets)
        rate  = cardinality / hours if cardinality else 1
        rate  = (60 * 60) / ceil(rate)
        rate -= 22 if 0 <= rate - 22 else 0
        distance = abs(22 - rate)
        m, n = max(0, (rate - distance)), max(1, (rate + distance))
        m, n = int(m), int(n)
        if (recursion < 4) and (rate - 22 < 0): return False
        n = random.randint(m, n)
        return n
