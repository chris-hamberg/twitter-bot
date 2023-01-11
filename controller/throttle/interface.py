from controller.throttle.sentinel import EngagementSentinel
from model.objects.exceptions import SentinelException
from model.objects.normalize import normalize, encode
from datetime import datetime
import logging


log = logging.getLogger(__name__)


class Throttle:


    def __init__(self): self._sentinel = EngagementSentinel()


    def enforce(self, manager, admin, warning):
        self._state(manager, admin, warning)
        if self._followerQ():                return True
        if (self.manager.name == "quantum"): return False
        delta, name = self._splitter()
        try: x, delta = self._engagement(delta)
        except SentinelException: return True
        if ((self.manager.name == "reply_type1") and (x)): return False
        elif (not delta): delta = self._delta(self.manager.name)
        if self._sleep(): return True
        elif ((delta) and (datetime.utcnow() <= delta)): return self._c(delta)
        else: return False


    def _c(self, delta):
        self.admin.orm.api.messages.create("rate limit", self.manager.name)
        return True


    def _state(self, manager, admin, warning):
        self.manager            = manager
        self.admin              = admin
        self.warning            = warning


    def _report(self, message = None, delta = None, silent = False, name = None):
        if not message: message = encode(delta)
        self.admin.orm.api.messages.create(message, name or self.manager.name)
        if silent: return True
        log.error("{self.admin.name}\n{message}")


    def _followerQ(self):
        if not (self.manager.name == "quantum"): return False
        elif self.warning:
            self._report("Something is wrong. Check your Twitter account.")
            return True
        else: return False


    def _engagement(self, delta):
        C1 = self.manager.name == "tweet"
        C2 = self.manager.name == "reply_type1"
        C3 = self.manager.name == "reply_type2"
        C4 = self.manager.name == "mention"
        if not any([C1, C2, C3, C4]): return False, delta
        x = self._sentinel.enforce(self.manager, self.admin)
        delta = self._delta(self.manager.name)
        return x, delta


    def _splitter(self):
        C1 = self.manager.name == "mention"
        C2 = self.manager.name == "type_gamma"
        C3 = self.manager.name == "youtube"
        if (not C1) and (not C2) and (not C3): return False, None
        elif C3: d1n, d2n = "ystream", "playlist"
        else:    d1n, d2n = "mention", "type_gamma"
        t1, t2 = self._delta(d1n), self._delta(d2n)
        return min((t1, d1n), (t2, d2n), key = lambda d: d[0])


    def _delta(self, attr):
        delta = getattr(self.admin.orm.api.state, f"{attr}_delta")
        delta = normalize(delta)
        return delta


    def _sleep(self):
        C1 = self.manager.name == "type_alpha"
        C2 = self.manager.name == "friend"
        C3 = self.manager.name == "unfriend"
        if ((C1) and (not self.admin.orm.api.resources)):         return True
        elif ((C2) or (C3)):
            delta = self._delta(self.manager.name)
            count = f"{self.manager.name}_count"
            count = getattr(self.admin.orm.api.state, count)
            if ((400 <= count) and (datetime.utcnow() <= delta)): return True
