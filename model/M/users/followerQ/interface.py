from model.M.users.followerQ.super_followerQ import FollowerQSuperManager
from datetime import timedelta
from datetime import datetime
import random
import time


class FollowerQManager(FollowerQSuperManager):


    def __init__(self, admin):
        super().__init__(admin)


    def execute(self):
        alpha = self.admin.orm.api.state.follower_complete
        beta  = self.admin.orm.api.state.following_complete
        if not (alpha and beta): 
            self.admin.orm.api.messages.create("Awaiting data.", f"{self.name}")
            return False
        self._pvalidate(); self.report("Beginning inference.")
        queue = (self._unfollow_unfollowers, self._follow_followers, 
                self._type_alpha_governor, self._delta_followers)
        for process in queue: self._execute(process)
        else: self._close()


    def _unfollow_unfollowers(self):
        self._validate("followerQ")
        A, B, C, D = self._get_4_sets("follower", "followerQ", "unfriendQ")
        self._update_database("unfriendQ", D, "follower")
        self._update_database("follower", B, "followerQ")
        self.report(f"found {len(D):,} users that used to follow "
                    f"{self.admin.name}, but now do not.")
        time.sleep(3)
        

    def _follow_followers(self):
        self._validate("followingQ")
        A, B, C, D = self._get_4_sets("follower", "followingQ", "blacklist")
        friendQ    = self.admin.orm.api.users.read("friendQ", short = True)
        friends    = D - set(friendQ)
        self._update_database("friendQ", friends, "following")
        self._update_database("following", B, "followingQ")
        self.report(f"found {len(friends):,} followers of which "
                    f"{self.admin.name} does not follow back.")
        time.sleep(3)


    def _type_alpha_governor(self):
        A, B, C, D = self._get_4_sets("following", "follower", "unfriendQ")
        type_alpha = self.admin.orm.api.type_alpha.read(
                delta = datetime.utcnow(),
                following = True, quantum = True, short = True)
        unfriends = D - set(type_alpha)
        self.admin.orm.api.users.create("unfriendQ", unfriends)
        length = len(unfriends - set(C))
        self.report(f"found {length:,} users {self.admin.name} follows, "
                     "but they do not follow back.")
        time.sleep(3)


    def _delta_followers(self):
        A, B, C, _ = self._get_4_sets("follower","blacklist","unfriendQ",True)
        cancel = (set(A) - set(B)) & set(C)
        self.admin.orm.api.users.delete("unfriendQ", cancel)
        count = self.admin.orm.api.state.unfriendQ_count - len(cancel)
        if (count <= 0): self.admin.orm.api.state.unfriendQ_count = 0
        else: self.admin.orm.api.state.unfriendQ_count = count
        self.report(f"cancelling unfriend for {len(cancel):,} user(s) now "
                    f"following {self.admin.name} back.")


    def _close(self):
        self.admin.orm.api.state.follower_count  = (
                self.admin.orm.api.users.count( "follower"))
        self.admin.orm.api.state.following_count = (
                self.admin.orm.api.users.count("following"))
        self.admin.orm.api.state.unfriendQ_count = (
                self.admin.orm.api.users.count("unfriendQ"))
        self.admin.orm.api.state.friendQ_count   = (
                self.admin.orm.api.users.count(  "friendQ"))
        for p in ("follower", "following"):
            m = random.randint(20, 45)
            d = datetime.utcnow() + timedelta(minutes = m)
            setattr(self.admin.orm.api.state, f"{p}_delta", d)
            setattr(self.admin.orm.api.state, f"{p}_complete", False)
