from model.objects.exceptions import QueueException
from datetime import datetime
import random


class FriendQueue:


    def __init__(self, admin):
        self._admin = admin


    def fill(self, name):
        try: (ids, candidates), Q = self._prepare(name), []
        except QueueException: return True
        if (name == "friend"): Q, ids = self._priority_selection(ids,candidates)
        Q, _ = self._random_selection(ids, candidates, Q, name)
        self._create(name, Q)


    def _prepare(self, name):
        orm = self._admin.orm
        if orm.api.users.count(f"{name}Q"): 
            raise QueueException("Has enough data.")
        candidates = orm.api.type_alpha.read(datetime.utcnow(),
                following = False if (name == "friend") else True)
        if (name == "friend"):
            friends   = set([f[0] for f in orm.api.users.read("friendQ")])
            following = set([f[0] for f in orm.api.users.read("following")])
            ids       = friends | following
        else: ids = set([f[0] for f in orm.api.users.read("unfriendQ")])
        return ids, candidates


    def _priority_selection(self, ids, candidates):
        Q, candidates = list(), list(filter(lambda u: u[7] == 1, candidates))
        condition = lambda c: True
        method    = lambda i, c: c.pop(i)
        return self._selection(ids, candidates, Q, condition, method, 0)


    def _random_selection(self, ids, candidates, Q, name):
        if (name == "unfriend"): ids = self._unfriend_selection(ids)
        condition = lambda c: 0 < c
        method    = lambda i, c: c.pop(random.choice(range(len(c))))
        return self._selection(ids, candidates, Q, condition, method, 399)


    def _unfriend_selection(self, users):
        orm, q = self._admin.orm, "followers"
        return set([f[0] for f in orm.api.users.read(q)]) | set(users)


    def _selection(self, ids, candidates, Q, condition, method, c):
        while (len(Q) < 399) and len(candidates) and condition(c):
            user = method(0, candidates)
            if (user[0] in ids): continue
            Q.append(user); ids.add(user[0])
            c -= 1
        return Q, ids


    def _create(self, name, users):
        orm = self._admin.orm
        orm.api.users.create(f"{name}Q", users)
        count = orm.api.users.count(f"{name}Q")
        setattr(orm.api.state, f"{name}Q_count", count)
