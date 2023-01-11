#from model.M.engage.compositors.neural_responder_ai import NeuralResponderAI
from model.M.engage.hypercortex.interface import HyperCortexTypeAlpha
from model.M.engage.compositors.like_compositor import LikeCompositor
from model.M.engage.hybridization import Hybridization
from datetime import timedelta
from datetime import datetime
import logging
import random
import time


log = logging.getLogger(__name__)


class MentionsManager:


    def __init__(self, admin):
        self.hybrid = Hybridization(admin)
        self.like   = LikeCompositor(admin)
        self.admin  = admin
        self.name   = "mention"


    def execute(self):
        self._report(message = "Checking for mentions in database.")
        time.sleep(2)
        params, c = {"liked": False, "replied": True, "mentioned": True}, 0
        like      = self.admin.orm.api.tweets.read(type = "mention", **params)
        for c, mention in enumerate(like):
            self.like.tweets_by_ids([mention[0]], self.name)
            self.admin.orm.api.tweets.update(mention[0])
        params.update({"replied": False, "mentioned": False})
        if self._sentinel_type_1(): self._close(c, limit = True); return True
        replies = self.admin.orm.api.tweets.read(type = "mention", **params)
        self._sentinel_type_2()
        c = self._reply(replies, c)
        self._close(c)


    def _reply(self, replies, c):
        try: reply = replies[0]
        except IndexError: return c
        #ai = NeuralResponderAI(self.admin, self.name)
        ai = HyperCortexTypeAlpha(self.admin, self.name)
        conversation_id = reply[-2]
        ai.state(reply, c_id = conversation_id)
        state = ai.compose()
        self.like.tweets_by_ids([reply[0]], self.name)
        self.admin.orm.api.tweets.update(reply[0])
        if state: ai.send()
        return c + 1


    def _sentinel_type_1(self):
        count = self.admin.orm.api.state.reply_count
        count = 15 - count
        if count <= 0: return True


    def _sentinel_type_2(self): self.hybrid.monitor("mention")


    def _close(self, c, limit = False):
        self._report(c, limit)
        self._delta(limit)
        self.hybrid.close()


    def _report(self, c = None, limit = None, message = None):
        if not message: message = self._get_message(c, limit)
        if not message: return False
        log.debug(f"{self.admin.name}\n{message}")
        self.admin.orm.api.messages.create(message, self.name)
        time.sleep(2)


    def _get_message(self, c, limit = False):
        if c and limit: 
            msg =  f"Liked {c} mention(s.) Reply is rate limited."
        elif (not c) and limit: 
            msg = None
        else: 
            msg = f"Liked {c} mention(s.)" if c else None
        return msg


    def _delta(self, limit):
        if limit: delta = timedelta(minutes = random.randint(45, 90))
        else:     delta = timedelta(minutes = random.randint(10, 20))
        self.admin.orm.api.state.mention_delta = datetime.utcnow() + delta
