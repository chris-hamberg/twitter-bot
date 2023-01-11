from model.objects.exceptions import ForbiddenException
from model.M.super.titan import Titan


class FollowerManager(Titan):


    def __init__(self, admin, name):
        super().__init__(admin, name)
        self.params = {"id":admin.id, "auth":admin.auth}


    def execute(self):
        if self.problems(): return False
        page = {"page": self._get_pagination()}
        self.params.update(page)
        beta = self.admin.orm.api.users.count(f"{self.name}Q")
        try:
            r = self._handler(**self.params)
            delta = self.delta(alpha = 60, zeta = 420)
            self.admin.orm.api.users.create(  f"{self.name}Q",           r)
            setattr(self.admin.orm.api.state, f"{self.name}_pagination", r)
            setattr(self.admin.orm.api.state, f"{self.name}_delta",  delta)
            alpha = self.admin.orm.api.users.count(f"{self.name}Q")
            delta = alpha - beta
            self.report(f"{alpha - beta} users added to \u03C7Q from data "
                        f"source: {self._get_pagination()}")
            self.terminate()
        except ForbiddenException as HTTP_403: self.forbidden()
