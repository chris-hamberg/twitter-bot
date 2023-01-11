#from model.M.engage.compositors.neural_responder_ai import NeuralResponderAI
from model.M.engage.hypercortex.interface import HyperCortexTypeAlpha
from model.M.engage.compositors.like_compositor import LikeCompositor
from model.M.engage.hybridization import Hybridization
from model.M.engage.retweets import RetweetManager
from model.M.super.superclass import SuperManager

from model.objects.exceptions import RateLimitException
from model.objects.exceptions import ProtectedException
from model.objects.exceptions import ForbiddenException

import traceback
import random


class ReplyType1Subcore(SuperManager):


    def __init__(self, admin):
        super().__init__()
        self.hybrid   = Hybridization( admin)
        self._like    = LikeCompositor(admin)
        self._retweet = RetweetManager(admin)
        self.admin    = admin
        self.name     = "reply_type1"

    
    def delegation(self, tweet, α, β, δ, ε):
        neural, state, error = None, None, None
        if α: neural, state = self._type_alpha(   tweet); self.hybrid.close()
        if β: error         = self._type_beta (   tweet, error)
        if δ: error         = self._type_delta(ε, tweet, error)
        return neural, state, error


    def _type_alpha(self, tweet):
        self.hybrid.monitor("reply_type1")
        neural = HyperCortexTypeAlpha(self.admin, self.name)
        neural.state(tweet)
        return neural, neural.compose()


    def _type_beta(self, tweet, error):
        try: self._execute_retweet(tweet)
        except RateLimitException as error: error = traceback.format_exc()
        return error


    def _type_delta(self, ε, tweet, error):
        if not ((ε and (random.randrange(10) != 9)) or (not ε)): return error
        try: self._execute_like(tweet)
        except RateLimitException as error: error = traceback.format_exc()
        return error


    def _execute_like(self, tweet):
        self._like.tweets_by_ids([tweet[0]], self.name)
        count = self.admin.orm.api.state.like_subcycle_count
        self.admin.orm.api.state.like_subcycle_count = count + 1


    def _execute_reply(self, neural, state, γ):
        count = self.admin.orm.api.state.retweet_reply_count
        self.admin.orm.api.state.retweet_reply_count = count + 1
        if ((state) and (γ)): neural.send()


    def _execute_retweet(self, tweet):
        errors = [ProtectedException, ForbiddenException, AssertionError]
        errors.append(AttributeError)
        errors = tuple(errors)
        try:
            r = self._retweet.retweet(tweet, self.name)
            assert (200 <= r.status_code < 300)
        except errors as e: self.report(f"retweet HTTP: {e}")
