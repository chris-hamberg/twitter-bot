from model.M.users.friends.compositors.delta import delta as deltaT
from datetime import timedelta
from datetime import datetime
import random


class FriendState:


    def __init__(self, admin):
        self._admin = admin


    def update(self, user, name, status):
        orm = self._admin.orm
        self._update_xQ(user, name, orm)
        self._update_type_alpha(user, name, orm)
        self._update_following(user, name, orm)
        self._update_x(name, orm, status)


    def _update_x(self, name, orm, status):
        index = getattr(self._admin.orm.api.state, f"{name}_subcycle_index")
        message = (f"{self._admin.name}\n{name}_subcycle_index = {index}    "
                   f"status = {status}")
        if not index:
            if (name == "friend"):
                n = deltaT(self._admin, 2, 28)
            else:
                n = random.randint(1, 27)
            delta = datetime.utcnow() + timedelta(minutes = n)
        else:
            if (name == "friend"):
                n = deltaT(self._admin, 5, 120)
            else:
                n = random.randint(3, 117)
            delta = datetime.utcnow() + timedelta(seconds = n)
        if status:
            count = getattr(orm.api.state, f"{name}_count")
            setattr(orm.api.state, f"{name}_count", count + 1)
        setattr(orm.api.state, f"{name}_delta", delta)


    def _update_xQ(self, user, name, orm):
        orm.api.users.delete(f"{name}Q", user)
        q_count = getattr(orm.api.state, f"{name}Q_count")
        if (q_count != 0): setattr(orm.api.state, f"{name}Q_count", q_count - 1)


    def _update_following(self, user, name, orm):
        if (name == "friend"): 
            orm.api.users.create("following", user)
            orm.api.state.following_count = orm.api.state.following_count + 1
        else:
            orm.api.users.delete("following", user)
            orm.api.state.following_count = orm.api.state.following_count - 1


    def _update_type_alpha(self, user, name, orm):
        id, delta = user[0], datetime.utcnow()+timedelta(days=7)
        orm.api.type_alpha.update(id, delta, True if (name == "friend") else False)
