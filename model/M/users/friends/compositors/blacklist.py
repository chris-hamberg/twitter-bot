class Blacklist:


    def __init__(self, admin):
        self._admin = admin


    def update(self, user, name):
        orm = self._admin.orm
        if (name == "friend"): return False
        user   = list(user)
        ucount = user[5] = user[5] + 1
        user   = tuple(user)
        orm.api.users.state.update(user, ucount)
        if ucount < 3: return False
        orm.api.users.create("blacklist", user)
        orm.api.users.state.inactive_delta(user)
        orm.api.type_alpha.delete(user)
