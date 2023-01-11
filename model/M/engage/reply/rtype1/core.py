from model.M.engage.compositors.filter_compositor import FilterCompositor
from model.M.engage.reply.rtype1.state import ReplyType1StateManager
from model.M.engage.reply.rtype1.subcore import ReplyType1Subcore
from model.objects.exceptions import RateLimitException

from datetime import timedelta
from datetime import datetime
import random


class ReplyType1Core:


    def __init__(self, admin):
        self._state   = ReplyType1StateManager(admin)
        self._subcore = ReplyType1Subcore(admin) 
        self._filter  = FilterCompositor(admin)
        self.admin    = admin
        self.name     = "reply_type1"


    def engage(self, tweets, recursion = 0):
        state = self._set_internal_state(tweets, recursion)
        tweet, p, error, state, username = state
        if self._pSentinel(p, tweet, tweets, username, recursion): return False
        α, β, δ, ε, γ        = self._get_conditions(p)
        neural, state, error = self._subcore.delegation(tweet, α, β, δ, ε)
        self._error_handler(error); self.admin.orm.api.tweets.update(tweet[0])
        if ε: self._subcore._execute_reply(neural, state, γ)
        self.admin.orm.api.messages.create("Awaiting engagement.", "retweets")
        self._state_recursion(tweets, recursion, skip = False)


    def _set_internal_state(self, tweets, recursion):
        tweet, p, error, state = tweets[0], random.random() * 100, None, None
        if recursion: p *= 4
        try:
            u_id, t_id = tweet[2], tweet[0]
            username = self.admin.orm.api.tweets.user(id=u_id, tweet_id=t_id)
            username = username[0][2]
        except IndexError: username = None
        return tweet, p, error, state, username


    def _pSentinel(self, p, tweet, tweets, username, recursion):
        C1 = self.admin.orm.api.state.like_probability < p
        C2 = self._filter.filter(tweet[1], user = username)
        if any([C1, C2]):
            self.admin.orm.api.tweets.update(tweet[0])
            self._state_recursion(tweets, recursion)
            return True


    def _get_conditions(self, p):
        Γ  = random.choice(["reply", "retweet", "both"])
        δ  = p <= self.admin.orm.api.state.like_probability
        C1 = p <= self.admin.orm.api.state.retweet_probability
        C2 = ((Γ == "retweet") or (Γ == "both"))
        β  = all([C1, C2])
        C1 = p <= self.admin.orm.api.state.reply_probability
        C2 = ((Γ == "reply") or (Γ == "both"))
        α  = all([C1, C2])
        ε, γ = C1, C2
        return α, β, δ, ε, γ


    def _error_handler(self, error):
        if not error: return True
        n = random.randint(15, 30)
        delta = datetime.utcnow() + timedelta(minutes = n)
        self.admin.orm.api.state.reply_type1_delta = delta
        raise RateLimitException


    def _state_recursion(self, tweets, recursion, skip = True):
        throttle   = self._state.manage(tweets, skip=skip, recursion=recursion)
        conditions = [(not throttle), (recursion < 4)]
        if all(conditions): self.engage(tweets[1:], recursion = recursion + 1)
