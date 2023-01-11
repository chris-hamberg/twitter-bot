from model.M.users.friends.compositors.control import FriendControl
from model.M.super.superclass import SuperManager
from model.objects.exceptions import ForbiddenException
from model.objects.exceptions import ProtectedException
from model.objects.exceptions import FatalError
import random


class FriendManager(SuperManager):


    def __init__(self, admin, name):
        super().__init__()
        self.control = FriendControl(admin)
        self.admin   = admin
        self.name    = name
        self.params  = {"admin_id":admin.id, "auth":admin.auth, 
                "token":admin.bearer}


    def execute(self):
        self.control.validate(self.name)
        self.control.queue.fill(self.name)
        if not getattr(self.admin.orm.api.state, f"{self.name}_subcycle_index"):
            i = random.randint(1, 11)
            setattr(self.admin.orm.api.state, f"{self.name}_subcycle_index", i)
        i = getattr(self.admin.orm.api.state, f"{self.name}_subcycle_index")
        while self.admin.orm.api.users.count(f"{self.name}Q"):
            user = self.admin.orm.api.users.read(f"{self.name}Q")[0]
            if self.control.blacklisted(user, self.name): continue
            if not self.control.is_follower(user, self.name):
                status = self._friend(user)
                if status: setattr(self.admin.orm.api.state, 
                        f"{self.name}_subcycle_index", i - 1)
                self.control.blacklist.update(user, self.name)
                self.control.state.update(user, self.name, status)
                break


    def _friend(self, user):
        try:
            self.params.update({"id": user[0]})
            r = self._handler(**self.params)
            if (200 <= r.status_code < 300):
                if (self.name == "friend"):
                    data      = r.json().get("data")
                    following = data.get("following")
                    pending   = data.get("pending_follow")
                    if (not following) and pending:
                        self.admin.orm.api.users.create("blacklist", user)
                        self.admin.orm.api.users.state.error(user)
                        self.report(f"Can't {self.name} {user[1]} because he/she is suspended.")
                        return False
                    else:
                        self.report(f"{self.admin.name} {self.name}ed {user[1]}.")
                        return True
                else:
                    self.report(f"{self.admin.name} {self.name}ed {user[1]}.")
                    return True
            else: 
                self.report(f"HTTP {r.status_code} for @{user[2]}")
                return False
        except ForbiddenException:
            self.report(f"HTTP 403 Forbidden. @{user[2]} may be locked.")
            return False
        except ProtectedException:
            self.report(f"The account for @{user[2]} is likely protected.")
            return False
