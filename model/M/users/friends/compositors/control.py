from model.M.users.friends.compositors.delta import delta as deltaT
from model.M.users.friends.compositors.blacklist import Blacklist
from model.M.users.friends.compositors.state import FriendState
from model.M.users.friends.compositors.queue import FriendQueue
from model.objects.exceptions import FriendRequestThresholdException
from model.objects.exceptions import RateLimitException
from datetime import timedelta
from datetime import datetime
import logging
import random
import time


log = logging.getLogger(__name__)


class FriendControl:


    def __init__(self, admin):
        self._admin    = admin
        self.blacklist = Blacklist(admin)
        self.state     = FriendState(admin)
        self.queue     = FriendQueue(admin)


    def blacklisted(self, user, name):
        orm = self._admin.orm
        try:
            if (name == "unfriend"): return False
            user = orm.api.users.read("blacklist", user[0])[0]
            user, name, count = user[:3], user[1], user[5]
            assert (count < 3)
            return False
        except IndexError: return False
        except AssertionError:
            orm.api.users.delete("friendQ", user) 
            orm.api.state.friendQ_count = orm.api.users.count("friendQ")
            orm.api.type_alpha.delete(user)
            return True


    def is_follower(self, user, name):
        orm = self._admin.orm
        if (name == "friend"): return False
        try: count = orm.api.users.read("blacklist", user[0])[0][5]
        except IndexError: pass
        else:
            if 3 <= count: return False
        if orm.api.users.read("follower", user[0]):
            orm.api.users.delete("unfriendQ", user)
            return True
        else: return False


    def validate(self, name):

        orm, efficency = self._admin.orm, 399
        epsilon = orm.api.state.following_count - orm.api.state.follower_count 

        if (4999 <= epsilon) and (name == "friend"):
            orm.api.state.friend_delta = datetime.utcnow() + timedelta(days = 6)
            orm.api.state.friend_count = 0
            raise FriendRequestThresholdException
        
        if (name == "friend"):
            xQ, load = orm.api.users.count("unfriendQ"), 400
            if (load < xQ):
                percent   = load / xQ
                efficency = int(399 * percent)
                percent   = round(percent * 100, 2)
                message   = (f"\u03C7Q overload; operating at {percent}% "
                             f"efficency ({efficency}) (this is ok.)")
                orm.api.messages.create(message, name)
                log.debug(f"{self._admin.name}\n{message}")
                time.sleep(5)

        count = getattr(self._admin.orm.api.state, f"{name}_count")
        if (efficency <= count): 
            log.debug(f"{self._admin.name}\nname: {name}    e = {efficency}    "
                      f"count = {count}")
            self.close(name)


    def close(self, name):
        orm = self._admin.orm
        if (name == "friend"): n = deltaT(self._admin, 120, 126, supercycle = True)
        else: n = random.randint(117, 123)
        delta = datetime.utcnow() + timedelta(minutes = n)
        setattr(orm.api.state, f"{name}_delta", delta)
        setattr(orm.api.state, f"{name}_count", 0)
        raise RateLimitException
