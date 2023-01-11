from model.objects.exceptions import RateLimitException
from model.twitter.get_tweets import GetTweets
from datetime import timedelta
from datetime import datetime
import logging
import random
import time


log = logging.getLogger(__name__)


class UnfollowInactiveFollowers:


    def __init__(self, admin):
        self._get_tweets  = GetTweets().request
        self.admin = admin
        self.name  = "inactive"


    def execute(self):
        followers = self.admin.orm.api.users.read("follower")
        index     = self.admin.orm.api.state.inactive_index
        if (index < len(followers)):
            follower = followers[index]
            delete   = self._test(follower, index)
            if (delete == True): 
                message = (f"{follower[1]} inactive over 1 year. "
                            "Scheduled for termination.")
                self._delete(follower)
            elif (delete == None):
                message = f"{follower[1]} is active on Twitter."
            elif (delete == False):
                message = f"{follower[1]} is already scheduled for termination."
            self.admin.orm.api.messages.create(message, self.name)
            log.debug(f"{self.admin.name}\n{message}")
            index = (index + 1) % len(followers)
            self.admin.orm.api.state.inactive_index = index
            xQ, delta, efficency = self._calculate_delta()
            if (400 <= xQ):
                time.sleep(3)
                message = (f"\u03C7Q overload; operating at {efficency}% "
                            "efficency (this is ok.)")
                self.admin.orm.api.messages.create(message, self.name)
                log.debug(f"{self.admin.name}\n{message}")
            self.admin.orm.api.state.inactive_delta = delta

        else:
            self.admin.orm.api.state.inactive_index = 0


    def _calculate_delta(self):
        xQ        = self.admin.orm.api.users.count("unfriendQ")
        rate      = 423 / 2
        efficency = 1
        if (400  <= xQ): efficency = 400 / xQ
        rate     /= efficency
        distance  = abs(3 - rate)
        m, n      = max(3, (rate - distance)), (rate + distance)
        m, n      = int(m), int(n)
        n         = random.randint(m, n)
        delta     = datetime.utcnow() + timedelta(seconds = n)
        efficency = round(efficency * 100, 2)
        return xQ, delta, efficency


    def _delete(self, follower):
        self.admin.orm.api.users.state.inactive_delta(follower)
        self.admin.orm.api.users.create("unfriendQ", [follower])
        self.admin.orm.api.users.create("blacklist", [follower])
        self.admin.orm.api.users.delete("friendQ", [follower])
        self.admin.orm.api.type_alpha.delete([follower])

        unfriendQ_count  = self.admin.orm.api.users.count("unfriendQ")
        friendQ_count    = self.admin.orm.api.users.count("friendQ")
        type_alpha_count = self.admin.orm.api.type_alpha.count()

        self.admin.orm.api.state.unfriendQ_count  = unfriendQ_count
        self.admin.orm.api.state.friendQ_count    = friendQ_count
        self.admin.orm.api.state.type_alpha_count = type_alpha_count


    def _test(self, follower, index):
        if self.admin.orm.api.users.read("unfriendQ", id = follower[0]):
            return False
        try:
            sentinel = self.admin.orm.api.users.read("blacklist", follower[0])
            assert sentinel[0][5] < 3, f"{sentinel[0][5]} < 3"
        except IndexError:
            pass
        except AssertionError:
            return True

        r = self._get_tweets(id = follower[0], auth = self.admin.auth, 
                max_results = 5, created_at = True)
        if not hasattr(r, "status_code"):
            return None
            return None
        elif (r.json().get("data")):
            ts = r.json().get("data")[0].get("created_at")
            ts = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.000Z")
            year = datetime.utcnow() - timedelta(weeks = 52)
            if ts <= year:
                return True
            return None
        return True


    def _close(self, index, count, count_inactive, r = None, force = False):
        delta, n, m = None, 0, ""
        try:
            assert index
            assert index % 37500
            if (r and r.status_code == 429):
                n, m = 15, "minutes"
                delta = datetime.utcnow() + timedelta(minutes = n)
                if (r and r.status_code == 429):
                    message = f"HTTP {r.status_code}: {self.name}"
                    self.admin.orm.api.messages.create(message, self.name)
                    log.debug(f"{self.admin.name}\n{message}")
                    time.sleep(3)
            elif force:
                n, m = 24, "hours"
                delta = datetime.utcnow() + timedelta(hours = n)
                message = ("Termination schedule is overloaded. "
                           f"Sleeping {n} hours.")
                self.admin.orm.api.messages.create(message, self.name)
                log.debug(f"{self.admin.name}\n{message}")
                time.sleep(3)
        except AssertionError:
            n, m = 5, "weeks"
            delta = datetime.utcnow() + timedelta(weeks = n)
        finally:
            if delta:
                if not force:
                    message = (f"of {count} followers: "
                               f"{count_inactive} scheduled for termination. "
                               f"Sleep {n} {m}.")
                    self.admin.orm.api.messages.create(message, self.name)
                    log.debug(f"{self.admin.name}\n{message}")
                self.admin.orm.api.state.inactive_delta = delta
                if (r and r.status_code == 429):
                    self.admin.orm.api.state.like_delta = delta
                time.sleep(3)
                raise RateLimitException


    def _validate(self):
        if 5000 <= self.admin.orm.api.state.unfriendQ_count:
            self._close(1, 0, 0, force = True)
